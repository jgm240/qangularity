# How Angularity FW updates work

qAngularity reads this file to find firmware:

    https://raw.githubusercontent.com/jgm240/angularity-fw/main/ota/directory.json

It uses the same JSON format as Flipper's own update server, so the download, sha256 check,
and BLE upload to the device are the upstream app's unchanged code.

## Publishing a new firmware version
1. Build the updater package (`./fbt updater_package` in the firmware repo).
2. Create a GitHub release in `jgm240/angularity-fw` tagged e.g. `AngularityFW-release26`
   and attach `flipper-z-f7-update-*.tgz` (rename it to something simple).
3. From this repo: `python3 tools/make_ota_directory.py --tgz <file> --tag <tag> --changelog "..." --out <angularity-fw>/ota/directory.json`
4. Commit and push `ota/directory.json` to `main` of the firmware repo.
