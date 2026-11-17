#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рендеры закрытого корпуса FOB-1 v2 и разнесённой сборки."""
from pathlib import Path
from cadquery import exporters
from render_final import render
import v2_full as m

TMP = Path("/tmp/fob_v2")
TMP.mkdir(exist_ok=True)
COLORS = {
    "cover": (0.20, 0.23, 0.27), "back": (0.28, 0.32, 0.37),
    "display": (0.025, 0.035, 0.05), "rtc": (0.12, 0.35, 0.60),
    "xiao_pcb": (0.10, 0.42, 0.28), "xiao_shield": (0.65, 0.68, 0.72),
    "usb": (0.25, 0.27, 0.30), "battery": (0.78, 0.69, 0.50),
    "foam": (0.10, 0.10, 0.10), "button": (0.12, 0.65, 0.32),
}

# Экспорт компонентов в исходном положении.
for name, part in m.parts.items():
    if name not in ("cover", "back"):
        exporters.export(part, str(TMP / f"{name}.stl"), tolerance=0.04, angularTolerance=0.2)

closed = [
    ("parts/v2_back.stl", COLORS["back"], 1.0),
    ("parts/v2_cover.stl", COLORS["cover"], 1.0),
]
for name in ("display", "rtc", "xiao_pcb", "xiao_shield", "usb", "battery", "foam", "button"):
    closed.append((str(TMP / f"{name}.stl"), COLORS[name], 1.0))
render(closed, "FOB-2_closed.png", size=(1800, 1200), ss=2,
       eye_dir=(0.62, -0.70, -0.48), up=(0, 0, 1))

# Разнесённая сборка: каждый узел остаётся рядом со своим посадочным местом.
offsets = {
    "back": 0.0, "battery": 10.0, "foam": 10.0,
    "xiao_pcb": 10.0, "xiao_shield": 10.0, "usb": 10.0,
    "rtc": 24.0, "display": 38.0, "cover": 51.0, "button": 51.0,
}
exploded = []
for name in ("back", "battery", "foam", "xiao_pcb", "xiao_shield", "usb", "rtc", "display", "cover", "button"):
    dz = offsets[name]
    shifted = m.parts[name].translate((0, 0, dz))
    path = TMP / f"exploded_{name}.stl"
    exporters.export(shifted, str(path), tolerance=0.04, angularTolerance=0.2)
    exploded.append((str(path), COLORS[name], 1.0))
render(exploded, "FOB-2_exploded.png", size=(1800, 1600), ss=2,
       eye_dir=(0.75, -0.80, -0.52), up=(0, 0, 1))

# Нижний слой без RTC и крышки: видны каналы XIAO и ложемент АКБ.
mounting = [
    ("parts/v2_back.stl", (0.68, 0.72, 0.76), 1.0),
    (str(TMP / "xiao_pcb.stl"), COLORS["xiao_pcb"], 1.0),
    (str(TMP / "xiao_shield.stl"), COLORS["xiao_shield"], 1.0),
    (str(TMP / "usb.stl"), COLORS["usb"], 1.0),
    (str(TMP / "battery.stl"), COLORS["battery"], 1.0),
    (str(TMP / "foam.stl"), COLORS["foam"], 1.0),
]
render(mounting, "FOB-2_mounting.png", size=(1800, 1200), ss=2,
       eye_dir=(0.60, -0.68, -0.62), up=(0, 0, 1))
render([("parts/v2_back.stl", (0.68, 0.72, 0.76), 1.0)],
       "FOB-2_back_inside.png", size=(1800, 1200), ss=2,
       eye_dir=(0.52, -0.70, -0.72), up=(0, 0, 1))
render([("parts/v2_cover.stl", (0.68, 0.72, 0.76), 1.0)],
       "FOB-2_cover_inside.png", size=(1800, 1200), ss=2,
       eye_dir=(0.52, -0.70, 0.72), up=(0, 0, 1))
print("FOB-2_closed.png, FOB-2_exploded.png, FOB-2_mounting.png, inside views")
