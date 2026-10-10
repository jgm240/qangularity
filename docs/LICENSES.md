# Third-party licenses and attributions

qAngularity is released under the MIT License (see `LICENSE`). It is derived from the
[Flipper Android app](https://github.com/flipperdevices/Flipper-Android-App) and
[Flipper iOS app](https://github.com/flipperdevices/Flipper-iOS-App), both MIT licensed,
(c) Flipper Devices Inc. Their notices are kept in `android/LICENSE` and `ios/LICENSE`.

qAngularity is unofficial and is not affiliated with or endorsed by Flipper Devices Inc.
"Flipper" and "Flipper Zero" are trademarks of their owners and are used only to name
compatible hardware.

## Fonts (reviewed 10 October 2026)

| Font | Used for | Author | License |
|---|---|---|---|
| Roboto (all weights) | Android UI text | Google | Apache License 2.0 - https://www.apache.org/licenses/LICENSE-2.0 |
| Roboto Mono | Android monospaced text | Google | Apache License 2.0 |
| Born2bSportyV2 | pixel-style numbers and labels (Android `flipper_bold.ttf`, `flipper_action.ttf`, `flipper.ttf`; iOS `Born2bSportyV2.ttf`) | JapanYoshi | Public Domain, as catalogued by the u8g2 project (https://github.com/olikraus/u8g2/blob/master/tools/font/build/fntgrpjapanyoshi.pre) |

### Removed font
The upstream apps also shipped **HaxrCorpNeue** (credited inside the file only as
"ValeriaAquamine"). No license could be verified for it, and it appears to be related to
"HaxrCorp 4089", which is licensed CC BY-SA 3.0. To avoid a license we could not confirm,
qAngularity does not ship it: Android's `flipper.ttf` is now Born2bSportyV2 and the iOS
`HaxrCorpNeue.ttf` was removed, with the same UI call sites using Born2bSportyV2.

## Other bundled artwork
- The illustrations of the Flipper Zero device used to mirror its screen are depictions of
  the hardware, kept so the app can show your device. Splash/launch logos and the app icon
  are original Angularity artwork (see `tools/make_icons.py`).

## Libraries
Android (Gradle) and iOS (Swift Package Manager) dependencies keep their own licenses, as
declared by each project. The dependency list has not been independently audited for this
fork; run your preferred license report (for example the Gradle license-report plugin) before
distributing binaries beyond personal use.
