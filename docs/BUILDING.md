# Building qAngularity

## Android (tested)
Requirements: JDK 21, Android SDK with `platforms;android-37.0` and `build-tools;37.0.0`.

```bash
export JAVA_HOME=/path/to/jdk-21
export ANDROID_HOME=/path/to/android-sdk
cd android
echo "sdk.dir=$ANDROID_HOME" > local.properties
./gradlew :instances:android:app:assembleDebug
# -> instances/android/app/build/outputs/apk/debug/app-debug.apk
```

The first build downloads Gradle 9.7 and all dependencies and takes roughly 10-15 minutes.
The protobuf and NFC-tools submodules of the upstream project are vendored into this
repository as plain files, so no `git submodule` step is needed.

Release builds are unsigned until you add a signing config; keep your keystore out of git.

## iOS / Mac Catalyst (NOT yet built)
Open `ios/Flipper/Flipper.xcodeproj` in Xcode, choose your own Team under Signing &
Capabilities for the app and widget targets, and run. The app and widgets share an App
Group, which requires a paid Apple Developer account. Mac Catalyst is enabled for the app and
the Live widget; the Live Activity extension is iOS-only.

## Regenerating icons
`python3 tools/make_icons.py` (needs `rsvg-convert` and Python).
