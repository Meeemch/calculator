#!/usr/bin/env bash
#
# Практическая работа 4 — сборка установочного пакета .pkg для macOS.
#
# Использование:
#   ./packaging/macos/build_pkg.sh [ВЕРСИЯ]
#
# Берёт скомпилированное приложение build/app/PyCalculator.app
# (если его нет — сначала компилирует через build_app.sh)
# и упаковывает в dist/PyCalculator-<ВЕРСИЯ>.pkg.
#
set -euo pipefail

##
## Параметры пакета (аналог шапки .spec-файла)
##
APP_NAME="PyCalculator"                     # имя .app
IDENTIFIER="com.meeemch.pycalculator"       # идентификатор пакета
VERSION="${1:-1.0}"                         # версия (параметр скрипта)
INSTALL_LOCATION="/Applications"            # куда ставить

info ()  { printf '\033[1m info: \033[0m %s\n' "$*"; }
ok ()    { printf '\033[1m done: \033[0m \033[32m%s\033[0m\n' "$*"; }
error () { printf '\033[1m ERROR:\033[0m \033[31m%s\033[0m\n' "$*" >&2; exit 1; }

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$HERE/../.." && pwd)"
BUILD_DIR="$PROJECT_DIR/build/pkg"
DIST_DIR="$PROJECT_DIR/dist"
ROOT_DIR="$BUILD_DIR/root"
COMPILED_APP="$PROJECT_DIR/build/app/$APP_NAME.app"
OUTPUT_PKG="$DIST_DIR/$APP_NAME-$VERSION.pkg"

command -v pkgbuild    >/dev/null || error "pkgbuild не найден (нужен macOS + Xcode Command Line Tools)"
command -v productbuild >/dev/null || error "productbuild не найден"

info "Сборка пакета $APP_NAME $VERSION"

##
## 1. Скомпилированное приложение
##
COMPILED_VERSION=""
if [ -d "$COMPILED_APP" ]; then
    COMPILED_VERSION="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' \
        "$COMPILED_APP/Contents/Info.plist" 2>/dev/null || true)"
fi
if [ "$COMPILED_VERSION" != "$VERSION" ]; then
    info "нет скомпилированного приложения версии $VERSION — компилирую"
    "$HERE/build_app.sh" "$VERSION" || error "компиляция не удалась"
fi

rm -rf "$BUILD_DIR"
mkdir -p "$ROOT_DIR" "$DIST_DIR"
info "копирование $APP_NAME.app в корень пакета"
cp -R "$COMPILED_APP" "$ROOT_DIR/"
find "$ROOT_DIR" -name '.DS_Store' -delete
xattr -cr "$ROOT_DIR" 2>/dev/null || true
ok "приложение готово к упаковке"

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
