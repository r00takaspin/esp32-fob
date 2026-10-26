#!/usr/bin/env bash
# Пересборка всех артефактов FOB-1.
# Требуется: cadquery, numpy, Pillow, python-docx, rsvg-convert.
set -euo pipefail

PY="${PY:-python3}"

echo "[1/4] 3D-модель (STEP/STL)…"
$PY v1_full.py

echo "[2/4] Схемы (SVG → PNG)…"
$PY wiring.py
$PY iso.py
$PY membrane_2wire_diagram.py
rsvg-convert -w 2400 -h 1697 FOB-1_payka.svg -o FOB-1_payka.png
rsvg-convert -w 2400 -h 1697 FOB-1_assembly_iso.svg -o FOB-1_assembly_iso.png
rsvg-convert -w 1600 -h 902 membrane_2wire_diagram.svg -o FOB-1_membrane_2wire.png

echo "[3/4] Документация (.docx)…"
$PY build_doc.py

echo "[4/4] 3D-рендер…"
$PY render_final.py

echo "Готово."
