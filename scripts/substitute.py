"""
Reads config.yml, copies remote/ to dist/, and replaces {{VAR}} placeholders.
Also applies multipliers to dmin/dmax in zombie_territories.xml and
nominal/min/max in events.xml for Infected event types.
"""
import math
import os
import re
import shutil
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "config.yml")
SRC_DIR = os.path.join(ROOT, "remote")
DST_DIR = os.path.join(ROOT, "dist")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Strip comments from config (yaml.safe_load already handles this)
variables = {k: str(v) for k, v in config.items()}

if os.path.exists(DST_DIR):
    shutil.rmtree(DST_DIR)
shutil.copytree(SRC_DIR, DST_DIR)

pattern = re.compile(r"\{\{(\w+)\}\}")
text_extensions = {".xml", ".json", ".cfg", ".txt", ".ini"}

for dirpath, _, filenames in os.walk(DST_DIR):
    for filename in filenames:
        if os.path.splitext(filename)[1].lower() not in text_extensions:
            continue
        filepath = os.path.join(dirpath, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        def replacer(match):
            key = match.group(1)
            if key not in variables:
                print(f"  WARNING: {{{{ {key} }}}} not found in config.yml ({filepath})")
                return match.group(0)
            return variables[key]

        new_content = pattern.sub(replacer, content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

print(f"Built dist/ with {len(variables)} variable(s) substituted.")

# --- Apply D multipliers to zombie_territories.xml ---

def _apply_d_multipliers(content, cfg):
    global_mult = float(cfg.get("INFECTED_GLOBAL_D_MULTIPLIER", 1.0))

    def replace_zone(m):
        tag = m.group(0)
        name_m = re.search(r'name="(\w+)"', tag)
        if not name_m:
            return tag
        name = name_m.group(1)
        type_mult = float(cfg.get(f"{name}_D_MULTIPLIER", 1.0))
        combined = global_mult * type_mult
        if combined == 1.0:
            return tag
        def scale(attr_m):
            val = int(attr_m.group(1))
            attr = attr_m.group(0).split("=")[0]
            new_val = 0 if val == 0 else math.ceil(val * combined)
            return f'{attr}="{new_val}"'
        tag = re.sub(r'dmin="(\d+)"', scale, tag)
        tag = re.sub(r'dmax="(\d+)"', scale, tag)
        return tag

    return re.sub(r'<zone\b[^>]*/>', replace_zone, content)

zt_path = os.path.join(DST_DIR, "dayzxb_missions", "dayzOffline.sakhal", "env", "zombie_territories.xml")
if os.path.exists(zt_path):
    with open(zt_path, "r", encoding="utf-8") as f:
        zt_content = f.read()
    zt_content = _apply_d_multipliers(zt_content, config)
    with open(zt_path, "w", encoding="utf-8") as f:
        f.write(zt_content)
    print("Applied D multipliers to zombie_territories.xml.")

# --- Apply multipliers to events.xml nominal/min/max ---

def _apply_event_multipliers(content, cfg):
    global_mult = float(cfg.get("INFECTED_GLOBAL_D_MULTIPLIER", 1.0))

    def replace_event(m):
        name = m.group(1)
        block = m.group(2)
        type_mult = float(cfg.get(f"{name}_D_MULTIPLIER", 1.0))
        combined = global_mult * type_mult
        if combined == 1.0:
            return m.group(0)
        def scale(tag_m):
            tag = tag_m.group(1)
            val = int(tag_m.group(2))
            return f"<{tag}>{math.ceil(val * combined)}</{tag}>"
        block = re.sub(r"<(nominal|min|max)>(\d+)</\1>", scale, block)
        return f'<event name="{name}">{block}</event>'

    return re.sub(
        r'<event name="(Infected\w+)">(.*?)</event>',
        replace_event,
        content,
        flags=re.DOTALL,
    )

ev_path = os.path.join(DST_DIR, "dayzxb_missions", "dayzOffline.sakhal", "db", "events.xml")
if os.path.exists(ev_path):
    with open(ev_path, "r", encoding="utf-8") as f:
        ev_content = f.read()
    ev_content = _apply_event_multipliers(ev_content, config)
    with open(ev_path, "w", encoding="utf-8") as f:
        f.write(ev_content)
    print("Applied multipliers to events.xml.")
