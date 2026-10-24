#!/usr/bin/env bash
#   1. загрузка актуального состояния с сервера (git pull)
#   2. сборка проекта и сборка unittest
#   3. выполнение unittest (pytest)
#   4. создание установщика (.pkg, см. packaging/macos/build_pkg.sh)
#   5. установка приложения (installer)
set -euo pipefail

info ()  { printf '\033[1m info: \033[0m %s\n' "$*"; }
ok ()    { printf '\033[1m done: \033[0m \033[32m%s\033[0m\n' "$*"; }
error () { printf '\033[1m ERROR:\033[0m \033[31m%s\033[0m\n' "$*" >&2; exit 1; }
stage () { printf '\n\033[1;34m==== Этап %s ====\033[0m\n' "$*"; }

BRANCH="main"
VERSION=""
SKIP_INSTALL=0
while getopts "b:v:sh" opt; do
    case "$opt" in
        b) BRANCH="$OPTARG" ;;
        v) VERSION="$OPTARG" ;;
        s) SKIP_INSTALL=1 ;;
        h) sed -n '2,19p' "$0"; exit 0 ;;
        *) error "неизвестный параметр, см. ./ci.sh -h" ;;
    esac
done

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"
PYTHON="${PYTHON:-python3}"
VENV="$PROJECT_DIR/.venv"
REPORTS="$PROJECT_DIR/build/reports"
START=$(date +%s)


stage "1/5: загрузка актуального состояния с сервера"
command -v git >/dev/null || error "git не установлен"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || error "$PROJECT_DIR не git-репозиторий"

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    info "Есть незакоммиченные изменения"
fi

info "git fetch origin"
git fetch --prune origin || error "не удалось получить данные с сервера"
info "git checkout $BRANCH"
git checkout "$BRANCH" || error "не удалось переключиться на $BRANCH"
info "git pull --ff-only origin $BRANCH"
git pull --ff-only origin "$BRANCH" || error "git pull не удался"
COMMIT="$(git rev-parse --short HEAD)"
ok "ветка $BRANCH, коммит $COMMIT"

[ -n "$VERSION" ] || VERSION="1.0.$(git rev-list --count HEAD)"
info "версия сборки: $VERSION"


stage "2/5: сборка проекта и сборка unittest"
command -v "$PYTHON" >/dev/null || error "$PYTHON не найден"
"$PYTHON" -c "import tkinter" 2>/dev/null || error "в $PYTHON нет модуля tkinter"

if [ ! -x "$VENV/bin/python" ]; then
    info "создание виртуального окружения"
    "$PYTHON" -m venv "$VENV" || error "не удалось создать .venv"
fi
info "установка зависимостей (requirements-dev.txt)"
"$VENV/bin/python" -m pip install --quiet --upgrade pip >/dev/null 2>&1 || true
"$VENV/bin/python" -m pip install --quiet -r requirements-dev.txt || error "pip install не удался"

info "компиляция исходников проекта"
"$VENV/bin/python" -m py_compile main.py arithmetic.py math_functions.py \
    || error "ошибка компиляции проекта"
ok "проект собран"

info "компиляция и сборка unittest"
"$VENV/bin/python" -m compileall -q tests || error "ошибка компиляции тестов"
"$VENV/bin/python" -m pytest --collect-only -q >/dev/null || error "тесты не собираются (ошибка импорта?)"
TESTS_COUNT=$("$VENV/bin/python" -m pytest --collect-only -q 2>/dev/null | grep -c '::' || true)
ok "unittest собраны: $TESTS_COUNT тестов"


stage "3/5: выполнение unittest"
mkdir -p "$REPORTS"
if "$VENV/bin/python" -m pytest -v --junitxml="$REPORTS/junit.xml"; then
    ok "все тесты пройдены (отчёт: build/reports/junit.xml)"
else
    error "тесты упали"
fi


stage "4/5: создание установщика"
"$PROJECT_DIR/packaging/macos/build_pkg.sh" "$VERSION" || error "не удалось собрать .pkg"
PKG="$PROJECT_DIR/dist/PyCalculator-$VERSION.pkg"
[ -f "$PKG" ] || error "файл $PKG не найден"
ok "установщик: dist/PyCalculator-$VERSION.pkg ($(du -h "$PKG" | cut -f1))"

stage "5/5: установка приложения"
if [ "$SKIP_INSTALL" -eq 1 ]; then
    info "установка пропущена (-s)"
else
    info "sudo installer -pkg $PKG -target /   (потребуется пароль)"
    sudo installer -pkg "$PKG" -target / || error "установка не удалась"

    info "проверка установки"
    [ -d /Applications/PyCalculator.app ] || error "нет /Applications/PyCalculator.app"
    INSTALLED=$(pkgutil --pkg-info com.meeemch.pycalculator | awk '/^version:/ {print $2}')
    [ "$INSTALLED" = "$VERSION" ] || error "установлена версия '$INSTALLED', ожидалась '$VERSION'"
    ok "PyCalculator $INSTALLED установлен в /Applications"
    info "запуск: open -a PyCalculator   или   pycalculator"
fi

printf '\n\033[1;32mCI успешно завершён за %s с (коммит %s, версия %s)\033[0m\n' \
    "$(( $(date +%s) - START ))" "$COMMIT" "$VERSION"
