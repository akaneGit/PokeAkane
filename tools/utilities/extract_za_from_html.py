import argparse
import json
import os
import re
from html.parser import HTMLParser
from typing import List, Tuple, Optional, Dict

NUMBER_CLASS = "style-module__pokemonNumberLabel___2ru5c"
NAME_CLASS = "style-module__pokemonName___d76mq"

# Keywords to identify regional forms to skip
REGIONAL_KEYWORDS = [
    "アローラ", "ガラル", "ヒスイ", "パルデア", "原種以外", "原種ではない", "リージョン", "地方", "ローカル"
]

class ZAHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_number_span = False
        self.in_name_span = False
        self.in_anchor = False
        self.current_number: Optional[str] = None
        self.current_name_parts: List[str] = []
        self.results: List[Tuple[int, str]] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'span' and attrs_dict.get('class') == NUMBER_CLASS:
            self.in_number_span = True
        elif tag == 'span' and attrs_dict.get('class') == NAME_CLASS:
            self.in_name_span = True
        elif tag == 'a' and self.in_name_span:
            self.in_anchor = True

    def handle_endtag(self, tag):
        if tag == 'span':
            # If closing a name span, finalize record
            if self.in_name_span:
                name = ''.join(self.current_name_parts).strip()
                if self.current_number and name:
                    # Skip regional forms by keywords
                    if not any(k in name for k in REGIONAL_KEYWORDS):
                        num = normalize_number(self.current_number)
                        if num is not None:
                            self.results.append((num, name))
                self.current_name_parts = []
            # Reset flags appropriately
            self.in_number_span = False if self.in_number_span else self.in_number_span
            self.in_name_span = False if self.in_name_span else self.in_name_span
        elif tag == 'a' and self.in_anchor:
            self.in_anchor = False

    def handle_data(self, data):
        if self.in_number_span:
            self.current_number = data.strip()
        elif self.in_anchor:
            self.current_name_parts.append(data)


def normalize_number(text: str) -> Optional[int]:
    # Extract digits from patterns like "No.1", "No.001"
    m = re.search(r"No\.?\s*([0-9０-９]+)", text)
    if not m:
        return None
    num_str = m.group(1)
    # Convert full-width digits to half-width
    trans = str.maketrans('０１２３４５６７８９', '0123456789')
    num_str = num_str.translate(trans)
    try:
        return int(num_str)
    except ValueError:
        return None


def load_existing_za(path: str) -> Dict:
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def merge_into_23(existing: Dict, extracted: List[Tuple[int, str]]) -> Dict:
    # Ensure structure
    if not existing:
        existing = {
            "id": 23,
            "name": "異次元図鑑（レジェンド Z-A）",
            "key": "za-alt",
            "pokemon": {}
        }
    pokemon = existing.setdefault("pokemon", {})
    for num, name in extracted:
        key = str(num)
        entry = pokemon.get(key)
        if not entry:
            pokemon[key] = {"name": name}
        else:
            # If existing, prefer existing name; only fill missing
            if "name" not in entry or not entry["name"]:
                entry["name"] = name
    return existing


def main():
    parser = argparse.ArgumentParser(description="Extract ZA dex entries from HTML and optionally update 23.json")
    parser.add_argument("html_path", help="Path to the source HTML/XML file")
    parser.add_argument("--update-json", dest="json_path", default=None, help="If provided, update this 23.json path")
    args = parser.parse_args()

    with open(args.html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    parser_obj = ZAHtmlParser()
    parser_obj.feed(content)
    extracted = parser_obj.results

    # Deduplicate by number, prefer first occurrence (assumed to be base form)
    dedup: Dict[int, str] = {}
    for num, name in extracted:
        if num not in dedup:
            dedup[num] = name
    extracted_unique = sorted([(n, dedup[n]) for n in dedup.keys()], key=lambda x: x[0])

    print(json.dumps([{"number": n, "name": nm} for n, nm in extracted_unique], ensure_ascii=False, indent=2))

    if args.json_path:
        existing = load_existing_za(args.json_path)
        merged = merge_into_23(existing, extracted_unique)
        with open(args.json_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        print(f"Updated {args.json_path} with {len(extracted_unique)} entries.")


if __name__ == "__main__":
    main()
