#!/usr/bin/env bash
#
# Практическая работа 4 — сборка установочного пакета .pkg для macOS.
#
# Использование:
#   ./packaging/macos/build_pkg.sh [ВЕРСИЯ]
#
# Результат: dist/PyCalculator-<ВЕРСИЯ>.pkg
# Пакет ставит /Applications/PyCalculator.app и команду /usr/local/bin/pycalculator.
#
set -euo pipefail

##
## Параметры пакета (аналог шапки .spec-файла)
##
APP_NAME="PyCalculator"                     # имя .app
DISPLAY_NAME="Калькулятор (Python)"         # имя, видимое пользователю
IDENTIFIER="com.meeemch.pycalculator"       # идентификатор пакета
VERSION="${1:-1.0}"                         # версия (параметр скрипта)
INSTALL_LOCATION="/Applications"            # куда ставить
APP_FILES="main.py arithmetic.py math_functions.py"   # исходники приложения

info ()  { printf '\033[1m info: \033[0m %s\n' "$*"; }
ok ()    { printf '\033[1m done: \033[0m \033[32m%s\033[0m\n' "$*"; }
error () { printf '\033[1m ERROR:\033[0m \033[31m%s\033[0m\n' "$*" >&2; exit 1; }

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$HERE/../.." && pwd)"
BUILD_DIR="$PROJECT_DIR/build/pkg"
DIST_DIR="$PROJECT_DIR/dist"
ROOT_DIR="$BUILD_DIR/root"
APP_DIR="$ROOT_DIR/$APP_NAME.app"
OUTPUT_PKG="$DIST_DIR/$APP_NAME-$VERSION.pkg"

command -v pkgbuild    >/dev/null || error "pkgbuild не найден (нужен macOS + Xcode Command Line Tools)"
command -v productbuild >/dev/null || error "productbuild не найден"

info "Сборка $APP_NAME $VERSION"
rm -rf "$BUILD_DIR"
mkdir -p "$APP_DIR/Contents/MacOS" "$APP_DIR/Contents/Resources/app" "$DIST_DIR"

##
## 1. Собираем .app-бандл
##
info "копирование исходников"
for f in $APP_FILES; do
    [ -f "$PROJECT_DIR/$f" ] || error "нет файла $f"
    cp "$PROJECT_DIR/$f" "$APP_DIR/Contents/Resources/app/"
done

info "создание Info.plist"
cat > "$APP_DIR/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>               <string>$APP_NAME</string>
    <key>CFBundleDisplayName</key>        <string>$DISPLAY_NAME</string>
    <key>CFBundleIdentifier</key>         <string>$IDENTIFIER</string>
    <key>CFBundleVersion</key>            <string>$VERSION</string>
    <key>CFBundleShortVersionString</key> <string>$VERSION</string>
    <key>CFBundleExecutable</key>         <string>$APP_NAME</string>
    <key>CFBundlePackageType</key>        <string>APPL</string>
    <key>LSMinimumSystemVersion</key>     <string>10.13</string>
    <key>NSHighResolutionCapable</key>    <true/>
</dict>
</plist>
PLIST

info "создание запускающего скрипта"
cat > "$APP_DIR/Contents/MacOS/$APP_NAME" <<'LAUNCHER'
#!/bin/bash
# Запуск калькулятора: ищем python3, в котором есть tkinter.
APP_RES="$(cd "$(dirname "$0")/../Resources/app" && pwd)"
for py in /opt/homebrew/bin/python3 /usr/local/bin/python3 \
          /Library/Frameworks/Python.framework/Versions/Current/bin/python3 \
          /usr/bin/python3; do
    if [ -x "$py" ] && "$py" -c "import tkinter" >/dev/null 2>&1; then
        cd "$APP_RES" && exec "$py" main.py "$@"
    fi
done
osascript -e 'display alert "Калькулятор" message "Не найден Python 3 с модулем tkinter. Установите Python с python.org."' >/dev/null 2>&1
echo "Не найден Python 3 с модулем tkinter" >&2
exit 1
LAUNCHER
chmod 755 "$APP_DIR/Contents/MacOS/$APP_NAME"

# убираем мусор и расширенные атрибуты, чтобы они не попали в пакет
find "$ROOT_DIR" \( -name '__pycache__' -o -name '.DS_Store' \) -prune -exec rm -rf {} +
xattr -cr "$ROOT_DIR" 2>/dev/null || true
ok "бандл $APP_NAME.app собран"

##
## 2. Компонентный пакет (pkgbuild)
##
info "pkgbuild"
COMPONENT_PLIST="$BUILD_DIR/component.plist"
pkgbuild --analyze --root "$ROOT_DIR" "$COMPONENT_PLIST" >/dev/null
# запрещаем "перемещение" бандла: иначе installer может обновить копию в build/ вместо /Applications
plutil -replace BundleIsRelocatable -bool NO "$COMPONENT_PLIST" 2>/dev/null \
  || /usr/libexec/PlistBuddy -c "Set :0:BundleIsRelocatable false" "$COMPONENT_PLIST"
chmod 755 "$HERE/scripts/postinstall"

pkgbuild \
    --root "$ROOT_DIR" \
    --component-plist "$COMPONENT_PLIST" \
    --identifier "$IDENTIFIER" \
    --version "$VERSION" \
    --install-location "$INSTALL_LOCATION" \
    --scripts "$HERE/scripts" \
    "$BUILD_DIR/$APP_NAME-component.pkg" >/dev/null
ok "компонентный пакет готов"

##
## 3. Итоговый установщик с окнами мастера (productbuild)
##
info "productbuild"
sed -e "s/@VERSION@/$VERSION/g" \
    -e "s/@IDENTIFIER@/$IDENTIFIER/g" \
    -e "s/@APP_NAME@/$APP_NAME/g" \
    "$HERE/Distribution.xml" > "$BUILD_DIR/Distribution.xml"

productbuild \
    --distribution "$BUILD_DIR/Distribution.xml" \
    --resources "$HERE/resources" \
    --package-path "$BUILD_DIR" \
    "$OUTPUT_PKG" >/dev/null

ok "установщик: $OUTPUT_PKG"
