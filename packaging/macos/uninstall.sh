#!/bin/bash
# Удаление установленного пакета. Запуск: sudo ./packaging/macos/uninstall.sh
set -e
rm -rf /Applications/PyCalculator.app
rm -f /usr/local/bin/pycalculator
pkgutil --forget com.meeemch.pycalculator 2>/dev/null || true
echo "PyCalculator удалён"
