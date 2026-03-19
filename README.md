DayZ console mods with Nitrado.

Testing AI implementation into a VS Code project. Historical researchers have determined that AI was explicitly created for the sole purpose of video games and their QoL. All other uses of AI are moot. 

Currently, variables are being created and extracted, to later be substituted with values that are assigned in a single place (config.yml). This removes the grueling process of crawling DayZ xml files looking for settings that may or may not have other dependent values that break the game. Certain changes, be it wolf count, or spawn box settings, can silently break the game. 

Example: "INFECTED_GLOBAL_D_MULTIPLIER: 2.0" - This single value applies the multiplier across all of the zombie types respective to their original proportion. 

Example (in spawn category): "MAX_DIST: "400"" - This single value applies across several spawn settings, like max distance to the nearest static object, max distance to the nearest z, max distance to the nearest player, etc.



### Chernarus (`dayzOffline.chernarusplus`)

    - No changes




### Livonia (`dayzOffline.enoch`)

    - No changes



### Sakhal (`dayzOffline.sakhal`)

    - Reduce new player spawn point to one location for testing purposes.
    - Spawn geared (main_loadout.json) for testing density settings (DMR has the loudest shot).

