#!/usr/bin/env python3
"""Generates every qAngularity icon asset (iOS/Mac Catalyst + Android) from one design.

Design: a sharp "A" built from a chevron (the angle) and a solid triangle in
the crossbar position. All coordinates are in a 108x108 box (Android's adaptive
icon canvas); the central ~66 units are the adaptive-icon safe zone.

Requires rsvg-convert (brew install librsvg). Run from anywhere:
    python3 tools/make_icons.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHEVRON = "54,30 74,76 63,76 54,55.3 45,76 34,76"
TRIANGLE = "54,63 59.5,76 48.5,76"
MARK = "#38E1FF"
ACCENT = "#FF8A1F"
BG_FLAT = "#0E1230"

CHEVRON_PATH = "M54,30 L74,76 L63,76 L54,55.3 L45,76 L34,76 Z"
TRIANGLE_PATH = "M54,63 L59.5,76 L48.5,76 Z"


def mark(scale=1.0):
    t = f'translate(54 54) scale({scale}) translate(-54 -54)'
    return (
        f'<g transform="{t}">'
        f'<polygon points="{CHEVRON}" fill="{MARK}"/>'
        f'<polygon points="{TRIANGLE}" fill="{ACCENT}"/>'
        f'</g>'
    )


def svg(body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108" '
        'width="108" height="108">' + body + '</svg>'
    )


IOS_SVG = svg(
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#0A0F24"/><stop offset="1" stop-color="#2A1160"/>'
    '</linearGradient></defs>'
    '<rect width="108" height="108" fill="url(#bg)"/>' + mark(1.3)
)
ANDROID_FG_SVG = svg(mark(1.0))
ANDROID_LEGACY_SVG = svg(
    f'<rect width="108" height="108" rx="24" fill="{BG_FLAT}"/>' + mark(1.15)
)


def render(svg_text, out, size):
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ['rsvg-convert', '-w', str(size), '-h', str(size), '-o', str(out)],
        input=svg_text.encode(), check=True,
    )


def main():
    # iOS / Mac Catalyst. Opaque, no alpha (App Store requirement).
    ios_dir = ROOT / 'ios/Flipper/Shared/Assets.xcassets/AppIcon.appiconset'
    for size in (40, 58, 60, 80, 87, 120, 180, 1024):
        render(IOS_SVG, ios_dir / f'icon-{size}.png', size)

    # Android.
    res = ROOT / 'android/components/core/ui/res/src/androidMain/res'
    densities = {'mdpi': 1.0, 'hdpi': 1.5, 'xhdpi': 2.0, 'xxhdpi': 3.0, 'xxxhdpi': 4.0}
    for name, factor in densities.items():
        render(ANDROID_FG_SVG, res / f'mipmap-{name}/ic_launcher_foreground.png', round(108 * factor))
        # Pre-API-26 launchers cannot read adaptive icons, so ship flat PNGs
        # (needed because the app now supports Android 6.0).
        render(ANDROID_LEGACY_SVG, res / f'mipmap-{name}/ic_launcher.png', round(48 * factor))

    (res / 'values/ic_launcher_background.xml').write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        f'    <color name="ic_launcher_background">{BG_FLAT}</color>\n</resources>\n'
    )

    def vector(chevron_color, triangle_color):
        return (
            '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            '        android:height="108dp"\n'
            '        android:viewportHeight="108"\n'
            '        android:viewportWidth="108"\n'
            '        android:width="108dp">\n'
            f'    <path android:fillColor="{chevron_color}" android:pathData="{CHEVRON_PATH}"/>\n'
            f'    <path android:fillColor="{triangle_color}" android:pathData="{TRIANGLE_PATH}"/>\n'
            '</vector>\n'
        )

    (res / 'drawable/ic_launcher_foreground.xml').write_text(vector(MARK, ACCENT))
    (res / 'drawable/ic_launcher_foreground_monochrome.xml').write_text(vector('#FFFFFF', '#FFFFFF'))


if __name__ == '__main__':
    main()
