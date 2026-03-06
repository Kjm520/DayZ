# DayZ Server Configuration

Custom server configuration files for DayZ offline/local play across multiple maps. Each map directory contains the full mission file structure used by the DayZ game server, with custom overrides applied where noted.

## Maps

### Chernarus (`dayzOffline.chernarusplus`)

The original DayZ map. No custom modifications — uses default vanilla configuration.

---

### Livonia (`dayzOffline.enoch`)

DayZ's second official map set in Eastern Europe. No custom modifications — uses default vanilla configuration.

---

### Sakhal (`dayzOffline.sakhal`)

DayZ's arctic island map. Custom overrides are maintained in the `custom/` subdirectory and take precedence over the base `db/` files.

**Custom files (`custom/`):**

- **`globals.xml`** — Adjusted global economy variables: increased zombie cap (1000), increased animal cap (200), raised initial spawn counts, and tweaked loot damage ranges.
- **`events.xml`** — Custom infected and animal spawn events defining population pools, nominal counts, and child type compositions for: army, heavy army, city, industrial, firefighter, medic, NBC, police, prisoner, religious, solitude, village zombie groups, plus bear and wolf animal events.
- **`types.xml`** — Custom loot type definitions overriding item spawn rates, quantities, and category assignments.
