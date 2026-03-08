"""
Parses remote/dayzxb_missions/dayzOffline.sakhal/db/types.xml
and outputs types.csv with columns: category, usage, name
Items with multiple usages get one row per usage.
Items with no category/usage get empty string in that column.
"""
import csv
import os
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML_PATH = os.path.join(ROOT, "remote", "dayzxb_missions", "dayzOffline.sakhal", "db", "types.xml")
CSV_PATH = os.path.join(ROOT, "types.csv")

tree = ET.parse(XML_PATH)
rows = []

for type_el in tree.getroot().findall("type"):
    name = type_el.get("name", "")
    category_el = type_el.find("category")
    category = category_el.get("name", "") if category_el is not None else ""
    usages = [u.get("name", "") for u in type_el.findall("usage")]

    if usages:
        for usage in usages:
            rows.append((category, usage, name))
    else:
        rows.append((category, "", name))

rows.sort(key=lambda r: (r[0], r[1], r[2]))

with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["category", "usage", "name"])
    writer.writerows(rows)

print(f"Written {len(rows)} rows to types.csv")
