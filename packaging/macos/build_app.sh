#!/usr/bin/env bash
#
# Компиляция калькулятора в нативное приложение macOS.
#
# Nuitka переводит Python-код (main.py, arithmetic.py, math_functions.py)
# в код на C, затем clang компилирует его в машинный код. Результат —
# PyCalculator.app с исполняемым файлом, которому не нужен установленный Python.
#
# Использование:
#   ./packaging/macos/build_app.sh [ВЕРСИЯ]
# Результат: build/app/PyCalculator.app
#
set -euo pipefail

APP_NAME="PyCalculator"
DISPLAY_NAME="Калькулятор (Python)"
IDENTIFIER="com.meeemch.pycalculator"
VERSION="${1:-1.0}"

info ()  { printf '\033[1m info: \033[0m %s\n' "$*"; }
ok ()    { printf '\033[1m done: \033[0m \033[32m%s\033[0m\n' "$*"; }
error () { printf '\033[1m ERROR:\033[0m \033[31m%s\033[0m\n' "$*" >&2; exit 1; }

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$HERE/../.." && pwd)"
OUT_DIR="$PROJECT_DIR/build/nuitka"
APP_OUT="$PROJECT_DIR/build/app/$APP_NAME.app"

# Python для сборки: из .venv проекта, иначе системный python3
PY="${PYTHON_BUILD:-$PROJECT_DIR/.venv/bin/python}"
[ -x "$PY" ] || PY="$(command -v python3)" || error "python3 не найден"

command -v clang >/dev/null || error "нет компилятора clang — выполните: xcode-select --install"
"$PY" -c "import tkinter" 2>/dev/null || error "в $PY нет модуля tkinter"

if ! "$PY" -m nuitka --version >/dev/null 2>&1; then
    info "установка компилятора Nuitka"
    "$PY" -m pip install --quiet "nuitka>=2.0,<3" || error "не удалось установить Nuitka"
fi
info "Nuitka $("$PY" -m nuitka --version 2>/dev/null | head -n 1)"

rm -rf "$OUT_DIR" "$(dirname "$APP_OUT")"
mkdir -p "$OUT_DIR" "$(dirname "$APP_OUT")"

info "компиляция main.py -> C -> машинный код (первый раз — несколько минут)"
"$PY" -m nuitka \
    --standalone \
    --macos-create-app-bundle \
    --enable-plugin=tk-inter \
    --macos-app-name="$APP_NAME" \
    --macos-app-version="$VERSION" \
    --output-dir="$OUT_DIR" \
    --assume-yes-for-downloads \
    --remove-output \
    "$PROJECT_DIR/main.py" || error "компиляция не удалась"

BUILT="$(find "$OUT_DIR" -maxdepth 1 -name '*.app' | head -n 1)"
[ -n "$BUILT" ] || error "Nuitka не создала .app в $OUT_DIR"
mv "$BUILT" "$APP_OUT"

info "настройка Info.plist"
PLIST="$APP_OUT/Contents/Info.plist"
plutil -replace CFBundleIdentifier         -string "$IDENTIFIER"   "$PLIST"
plutil -replace CFBundleName               -string "$APP_NAME"     "$PLIST"
plutil -replace CFBundleDisplayName        -string "$DISPLAY_NAME" "$PLIST"
plutil -replace CFBundleShortVersionString -string "$VERSION"      "$PLIST"
plutil -replace CFBundleVersion            -string "$VERSION"      "$PLIST"

EXE="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' "$PLIST")"
[ -x "$APP_OUT/Contents/MacOS/$EXE" ] || error "нет исполняемого файла Contents/MacOS/$EXE"

# после правки Info.plist подпись нужно обновить (ad-hoc подпись без сертификата)
codesign --force --deep --sign - "$APP_OUT" >/dev/null 2>&1 \
    || info "не удалось подписать приложение (ad-hoc), продолжаем"
xattr -cr "$APP_OUT" 2>/dev/null || true

ok "скомпилировано: build/app/$APP_NAME.app ($(du -sh "$APP_OUT" | cut -f1))"
info "исполняемый файл: $(file -b "$APP_OUT/Contents/MacOS/$EXE")"
