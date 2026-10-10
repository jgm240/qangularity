# qAngularity

Fork of the official Flipper mobile apps (both MIT licensed, see `android/LICENSE`
and `ios/LICENSE`) that updates **Angularity FW** over the air instead of the
stock firmware.

| Folder    | Upstream                                   | Targets                                  |
|-----------|--------------------------------------------|------------------------------------------|
| `android` | flipperdevices/Flipper-Android-App (`dev`) | Android 6.0+ (minSdk 23)                 |
| `ios`     | flipperdevices/Flipper-iOS-App (`dev`)     | iPhone (iOS 16+) and Mac Catalyst        |
| `tools`   | -                                          | icon generator, OTA directory generator |

## Status

- **Android:** builds and produces an installable debug APK (see `docs/BUILDING.md`).
  Not yet exercised on real devices.
- **iOS / Mac Catalyst:** changes are made but **never compiled** (no Xcode was available).

## How OTA works

Both apps read `directory.json` (same schema as Flipper's own update server),
download the updater `.tgz`, check its sha256, and push it to the Flipper over
BLE exactly as upstream does. Only the source changed:

    https://raw.githubusercontent.com/jgm240/angularity-fw/main/ota/directory.json

To publish a release:

1. Create a GitHub release in `jgm240/angularity-fw` tagged e.g. `AngularityFW-release25`
   and attach `AngularityFW-release25.tgz` (the `flipper-z-f7-update-*.tgz` from `dist/f7-C`).
2. `python3 tools/make_ota_directory.py --tgz <that file> --tag <that tag> --changelog "..." --out <angularity-fw>/ota/directory.json`
3. Commit and push `ota/directory.json` to `main`.

## What changed vs upstream

Both
- OTA source -> Angularity (above)
- Name `qAngularity`, new app icon (`python3 tools/make_icons.py` regenerates all sizes)
- Bundle/application id `com.angularity.qangularity`
- Telemetry to Flipper's servers removed/disabled

Android
- `minSdk` 26 -> 23 (`ApkConfig.kt`). API-26-only calls guarded: notification
  channels (2 places), `java.time` in the device-info export.
  Legacy `mipmap-*dpi/ic_launcher.png` added because pre-26 can't read adaptive icons.
- Google/Firebase features off by default (`is_google_feature=false`); the bundled
  `google-services.json` is Flipper's project and is only kept so the plugin passes.
- App self-update check points at `jgm240/qangularity` releases (create that repo/release
  to use it; until then it just finds nothing).

iOS / Mac Catalyst
- `SUPPORTS_MACCATALYST = YES` on the app and the Live widget; Live Activities code is
  compiled out on Catalyst. ActivityWidget/KeyPreview were already iOS-only.
- Push notifications stubbed (upstream used Flipper's Firebase project).
- `DEVELOPMENT_TEAM` cleared - pick your own team in Xcode.

## Documents

- [Terms of Use](docs/TERMS.md)
- [Privacy Policy](docs/PRIVACY.md)
- [Building](docs/BUILDING.md)
- [OTA publishing](docs/OTA.md)
- [Licenses and font review](docs/LICENSES.md)

## Known gaps

- Android: only the call sites found by search were guarded. Run lint (`NewApi`) and a
  device test on API 23-25; dependencies may also need attention.
- The upstream cloud features (FapHub catalog, cloud key sync, infrared DB, region
  provisioning) still talk to Flipper Devices' servers, which is what makes them work.
- Mac Catalyst: BLE entitlements/capabilities need to be enabled for your team in Xcode.
