#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FOB-1 v2 — вариант A, разборный корпус с независимой фиксацией узлов.

Координаты: лицевая сторона крышки Z=0, внешнее дно стакана Z=T.
Все размеры в миллиметрах. Перед финальной печатью сверить раздел «измеренные
размеры» с фактически купленными компонентами.
"""
from pathlib import Path
import json
import cadquery as cq
from cadquery import exporters

OUT = Path("parts")
OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------ корпус
W, H, T, R = 48.0, 28.0, 19.0, 5.0
WALL, RC = 1.8, 3.2
Z_CAV0, Z_CAV1 = 2.0, 16.4
BOTTOM = T - Z_CAV1
CLEAR = 0.25

# Проушина принадлежит только стакану; крышка нагрузку кольца не несёт.
EAR_CENTER_X = -1.0
EAR_LENGTH = 15.0
EAR_WIDTH = 8.4
EAR_HOLE_X, EAR_HOLE_Y = -4.0, H / 2
RING_HOLE_D = 4.0
EYELET_D, EYELET_DEPTH = 3.6, 2.0

# ------------------------------------------------------- измеренные размеры
# Пока используются значения исходного BOM. Допуски добавлены отдельно.
OLED = dict(x=5.0, y=7.75, w=36.5, h=12.5, z=2.0, t=1.6)
OLED_WINDOW = dict(x=8.5, y=10.8, w=23.0, h=6.4)
RTC = dict(x=2.7, y=5.2, w=42.6, h=17.6, z=4.7, t=6.0)
XIAO = dict(x=24.0, y=5.1, w=21.0, h=17.8, z=11.2, pcb_t=1.0, total_t=3.2)
BATTERY = dict(x=3.0, y=4.0, w=11.0, h=20.0, z=11.2, t=4.0)
BATTERY_FOAM_T = 0.8
BUTTON = dict(x=40.5, y=14.0, d=7.0, recess_d=7.5, recess_t=0.35, wire_d=2.5)

# ---------------------------------------------------------------- helpers
def blk(x0, x1, y0, y1, z0, z1, radius=0.0):
    wp = (cq.Workplane("XY", origin=(0, 0, z0))
          .center((x0 + x1) / 2, (y0 + y1) / 2)
          .rect(x1 - x0, y1 - y0).extrude(z1 - z0))
    if radius:
        wp = wp.edges("|Z").fillet(radius)
    return wp


def cyl(d, x, y, z0, z1):
    return (cq.Workplane("XY", origin=(0, 0, z0))
            .center(x, y).circle(d / 2).extrude(z1 - z0))


def rounded(w, h, r, cx, cy, z0, z1):
    return blk(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2,
               z0, z1, r)


def outer_main(z0, z1):
    return rounded(W, H, R, W / 2, H / 2, z0, z1)


def ear(z0, z1):
    return (cq.Workplane("XY", origin=(0, 0, z0))
            .center(EAR_CENTER_X, EAR_HOLE_Y)
            .slot2D(EAR_LENGTH, EAR_WIDTH).extrude(z1 - z0))


def ring(outer_w, outer_h, inner_w, inner_h, z0, z1):
    outer = rounded(outer_w, outer_h, R - 0.8, W / 2, H / 2, z0, z1)
    inner = rounded(inner_w, inner_h, max(0.8, RC - 0.8), W / 2, H / 2, z0, z1)
    return outer.cut(inner)


def dict_block(p, total_key="t"):
    return blk(p["x"], p["x"] + p["w"], p["y"], p["y"] + p["h"],
               p["z"], p["z"] + p[total_key])


# --------------------------------------------------------------- крышка
cover = outer_main(0, 2.0).edges("<Z").fillet(1.0)

# Окно OLED и углубление под мембранную кнопку.
ow = OLED_WINDOW
cover = cover.cut(blk(ow["x"], ow["x"] + ow["w"],
                      ow["y"], ow["y"] + ow["h"], -0.5, 2.5, 0.6))
b = BUTTON
cover = cover.cut(cyl(b["recess_d"], b["x"], b["y"], -0.1, b["recess_t"]))
cover = cover.cut(cyl(b["wire_d"], b["x"] + 2.0, b["y"], -0.2, 2.4))

# Независимая рамка OLED: по 0,20 мм на сторону для лёгкой установки.
o = OLED
ox0, ox1 = o["x"], o["x"] + o["w"]
oy0, oy1 = o["y"], o["y"] + o["h"]
oz1 = o["z"] + o["t"]
fit = 0.20
fx0, fx1, fy0, fy1 = ox0 - fit, ox1 + fit, oy0 - fit, oy1 + fit
cover = cover.union(blk(fx0 - 0.45, fx0, fy0, fy1, 2.0, oz1 + 0.5))
cover = cover.union(blk(fx0, fx1, fy0 - 0.45, fy0, 2.0, oz1 + 0.35))
cover = cover.union(blk(fx0, fx1, fy1, fy1 + 0.45, 2.0, oz1 + 0.35))
cover = cover.union(blk(fx1, fx1 + 0.4, fy0, fy1, 2.0, oz1 + 0.35))
# Пружинные язычки за пределами посадочного контура; крюк — за задней гранью PCB.
for x0 in (14.0, 29.0):
    cover = cover.union(blk(x0, x0 + 6.0, fy0 - 0.85, fy0, 2.0, 4.45))
    cover = cover.union(blk(x0, x0 + 6.0, fy1, fy1 + 0.85, 2.0, 4.45))
    cover = cover.union(blk(x0, x0 + 6.0, fy0 - 0.85, fy0 + 0.35, oz1, oz1 + 0.4))
    cover = cover.union(blk(x0, x0 + 6.0, fy1 - 0.35, fy1 + 0.85, oz1, oz1 + 0.4))

# Выравнивающий бортик: по 0,20 мм зазора на каждую сторону паза.
LIP = dict(outer_w=W - 2.4, outer_h=H - 2.4, inner_w=W - 5.2, inner_h=H - 5.2)
cover = cover.union(ring(LIP["outer_w"], LIP["outer_h"],
                         LIP["inner_w"], LIP["inner_h"], 2.0, 3.0))

# Четыре разборные защёлки крышки. Пазы в стакане делаются ниже.
SNAP_X = ((13.0, 20.0), (28.0, 35.0))
SNAP_Z0, SNAP_Z1 = 2.0, 7.0
for x0, x1 in SNAP_X:
    # Нижняя сторона: язычок и крюк наружу.
    cover = cover.union(blk(x0, x1, 1.15, 1.95, SNAP_Z0, SNAP_Z1))
    cover = cover.union(blk(x0, x1, 0.65, 1.15, SNAP_Z1 - 0.85, SNAP_Z1))
    # Верхняя сторона, зеркально.
    cover = cover.union(blk(x0, x1, H - 1.95, H - 1.15, SNAP_Z0, SNAP_Z1))
    cover = cover.union(blk(x0, x1, H - 1.15, H - 0.65, SNAP_Z1 - 0.85, SNAP_Z1))

# Паз для аккуратного поддевания крышки.
cover = cover.cut(cyl(2.4, 24.0, 0.0, -0.2, 1.1))

# ---------------------------------------------------------------- стакан
back = outer_main(Z_CAV0, T).union(ear(Z_CAV0, T))
back = back.edges(">Z").fillet(1.0)
back = back.cut(rounded(W - 2 * WALL, H - 2 * WALL, RC,
                        W / 2, H / 2, Z_CAV0, Z_CAV1))
back = back.cut(cyl(RING_HOLE_D, EAR_HOLE_X, EAR_HOLE_Y, 1.5, T + 0.5))
# Посадка люверса с внешней стороны дна; кольцо нагружает стакан.
back = back.cut(cyl(EYELET_D, EAR_HOLE_X, EAR_HOLE_Y, T - EYELET_DEPTH, T + 0.5))

# Паз выравнивающего бортика +0,20 мм на сторону.
back = back.cut(ring(LIP["outer_w"] + 0.4, LIP["outer_h"] + 0.4,
                     LIP["inner_w"] - 0.4, LIP["inner_h"] - 0.4,
                     2.0, 3.15))

# Пазы и ответные уступы четырёх защёлок крышки.
for x0, x1 in SNAP_X:
    xx0, xx1 = x0 - 0.2, x1 + 0.2
    back = back.cut(blk(xx0, xx1, 0.95, 2.15, 2.0, SNAP_Z1 + 0.25))
    back = back.cut(blk(xx0, xx1, 0.45, 1.2, SNAP_Z1 - 1.0, SNAP_Z1 + 0.25))
    back = back.cut(blk(xx0, xx1, H - 2.15, H - 0.95, 2.0, SNAP_Z1 + 0.25))
    back = back.cut(blk(xx0, xx1, H - 1.2, H - 0.45, SNAP_Z1 - 1.0, SNAP_Z1 + 0.25))
back = back.cut(cyl(2.4, 24.0, 0.0, 1.8, 3.0))

# RTC: направляющие соединены со стенками, передние упоры — с направляющими.
r = RTC
rx0, rx1 = r["x"], r["x"] + r["w"]
ry0, ry1 = r["y"], r["y"] + r["h"]
rz0, rz1 = r["z"], r["z"] + r["t"]
back = back.union(blk(WALL, rx0, ry0 - 0.25, ry1 + 0.25, rz0 - 0.35, rz1 + 0.55))
back = back.union(blk(rx1, W - WALL, ry0 - 0.25, ry1 + 0.25, rz0 - 0.35, rz1 + 0.55))
for x0, x1 in ((4.0, 9.0), (39.0, 44.0)):
    for sy0, sy1 in ((ry0, ry0 + 2.0), (ry1 - 2.0, ry1)):
        back = back.union(blk(x0, x1, sy0, sy1, rz0 - 0.35, rz0))
        join_x0, join_x1 = (rx0 - 0.55, x0) if x0 < W / 2 else (x1, rx1 + 0.55)
        back = back.union(blk(join_x0, join_x1, sy0, sy1, rz0 - 0.35, rz0))
# Пружинные язычки RTC размещены вне контура платы.
for y0 in (7.0, 18.0):
    back = back.union(blk(rx0 - 0.85, rx0, y0, y0 + 4.0, rz0, rz1 + 0.55))
    back = back.union(blk(rx1, rx1 + 0.85, y0, y0 + 4.0, rz0, rz1 + 0.55))
    back = back.union(blk(rx0 - 0.85, rx0 + 0.35, y0, y0 + 4.0, rz1, rz1 + 0.4))
    back = back.union(blk(rx1 - 0.35, rx1 + 0.85, y0, y0 + 4.0, rz1, rz1 + 0.4))

# XIAO: П-образные продольные каналы. Плата вдвигается слева направо.
x = XIAO
xx0, xx1 = x["x"], x["x"] + x["w"]
xy0, xy1 = x["y"], x["y"] + x["h"]
xz0, xz1 = x["z"], x["z"] + x["pcb_t"]
channel_x0, channel_x1 = xx0 - 1.5, xx1 + 0.25
for yy0, yy1, ledge_y0, ledge_y1 in (
    (xy0 - 0.75, xy0 - 0.15, xy0 - 0.15, xy0 + 1.0),
    (xy1 + 0.15, xy1 + 0.75, xy1 - 1.0, xy1 + 0.15),
):
    back = back.union(blk(channel_x0, channel_x1, yy0, yy1, xz0 - 0.25, xz1 + 0.7))
    back = back.union(blk(channel_x0, channel_x1, ledge_y0, ledge_y1, xz0 - 0.25, xz0))
    back = back.union(blk(channel_x0, channel_x1, ledge_y0, ledge_y1, xz1, xz1 + 0.55))
# Торцевой упор USB разделён, чтобы не пересекаться с разъёмом.
for sy0, sy1 in ((xy0 - 0.15, 8.8), (19.2, xy1 + 0.15)):
    back = back.union(blk(xx1, xx1 + 0.55, sy0, sy1, xz0 - 0.25, xz1 + 0.7))
# Тонкий пружинный язычок соединён с перегородкой через нижнюю перемычку.
back = back.union(blk(22.0, xx0 - 0.35, 10.0, 14.0, Z_CAV1 - 0.6, Z_CAV1))
back = back.union(blk(xx0 - 0.9, xx0 - 0.35, 10.0, 14.0, xz0, Z_CAV1 - 0.4))
back = back.union(blk(xx0 - 0.35, xx0, 10.0, 14.0, xz0, xz1 + 0.35))

# Аккумулятор: отдельный ложемент, боковые стенки и мягкий компенсатор.
ba = BATTERY
bx0, bx1 = ba["x"], ba["x"] + ba["w"]
by0, by1 = ba["y"], ba["y"] + ba["h"]
bz0, bz1 = ba["z"], ba["z"] + ba["t"]
px0, px1 = bx0 - 0.5, bx1 + 0.5
py0, py1 = by0 - 0.5, by1 + 0.5
back = back.union(blk(px0 - 0.75, px0, py0 - 0.75, py1 + 0.75, bz0, Z_CAV1))
back = back.union(blk(px1, px1 + 0.75, py0 - 0.75, py1 + 0.75, bz0, Z_CAV1))
back = back.union(blk(px0, px1, py0 - 0.75, py0, bz0, Z_CAV1))
back = back.union(blk(px0, px1, py1, py1 + 0.75, bz0, Z_CAV1))
# Низкопрофильные язычки не зажимают банку, а только удерживают её в ложементе.
for yy0 in (6.0, 18.0):
    back = back.union(blk(px0 - 0.65, px0, yy0, yy0 + 4.0, bz0, Z_CAV1 - 0.25))
    back = back.union(blk(px1, px1 + 0.65, yy0, yy0 + 4.0, bz0, Z_CAV1 - 0.25))
    back = back.union(blk(px0 - 0.65, px0 + 0.3, yy0, yy0 + 4.0, bz0, bz0 + 0.35))
    back = back.union(blk(px1 - 0.3, px1 + 0.65, yy0, yy0 + 4.0, bz0, bz0 + 0.35))

# Перегородка между аккумулятором и XIAO, с местом для проводов сверху.
back = back.union(blk(20.8, 22.2, 3.0, 25.0, 13.0, Z_CAV1))
# USB-C: окно под реальный штекер, не только под металлический разъём.
back = back.cut(blk(45.4, W + 0.8, 8.8, 19.2, 10.8, 15.0, 0.5))

# ------------------------------------------------------ модели компонентов
display = dict_block(OLED)
rtc = dict_block(RTC)
xiao_pcb = blk(xx0, xx1, xy0, xy1, xz0, xz1, 0.8)
xiao_shield = blk(28.0, 41.0, 8.0, 20.0, xz1, xz0 + x["total_t"], 0.7)
usb = blk(44.5, 48.3, 9.5, 18.5, 11.3, 14.3, 0.5)
battery = dict_block(BATTERY)
foam = blk(px0 + 0.5, px1 - 0.5, py0 + 0.5, py1 - 0.5,
           bz1, bz1 + BATTERY_FOAM_T)
button = cyl(BUTTON["d"], BUTTON["x"], BUTTON["y"], -0.25, 0.0)

parts = {
    "cover": cover,
    "back": back,
    "display": display,
    "rtc": rtc,
    "xiao_pcb": xiao_pcb,
    "xiao_shield": xiao_shield,
    "usb": usb,
    "battery": battery,
    "foam": foam,
    "button": button,
}

# Печатные детали отдельно, полная сборка — одним STEP.
for name in ("cover", "back"):
    exporters.export(parts[name], str(OUT / f"v2_{name}.step"))
    exporters.export(parts[name], str(OUT / f"v2_{name}.stl"),
                     tolerance=0.02, angularTolerance=0.15)

assembly = cq.Assembly(name="FOB-1_v2")
colors = {
    "cover": (0.20, 0.23, 0.27), "back": (0.28, 0.32, 0.37),
    "display": (0.03, 0.05, 0.07), "rtc": (0.12, 0.35, 0.60),
    "xiao_pcb": (0.10, 0.42, 0.28), "xiao_shield": (0.65, 0.68, 0.72),
    "usb": (0.30, 0.32, 0.35), "battery": (0.78, 0.69, 0.50),
    "foam": (0.12, 0.12, 0.12), "button": (0.12, 0.65, 0.32),
}
for name, part in parts.items():
    assembly.add(part, name=name, color=cq.Color(*colors[name]))
assembly.save(str(OUT / "v2_assembly.step"))

# Отчёт для повторяемой проверки. Пересечения фиксируем, а не скрываем.
report = {"dimensions_mm": {"body": [W, H, T], "with_ear_nominal": [W + 8.5, H, T]},
          "clearance_mm": CLEAR,
          "layers": {"oled": [OLED["z"], OLED["z"] + OLED["t"]],
                     "rtc": [RTC["z"], RTC["z"] + RTC["t"]],
                     "xiao": [XIAO["z"], XIAO["z"] + XIAO["total_t"]],
                     "battery": [BATTERY["z"], BATTERY["z"] + BATTERY["t"]],
                     "foam": [BATTERY["z"] + BATTERY["t"],
                              BATTERY["z"] + BATTERY["t"] + BATTERY_FOAM_T]},
          "case_validity": {},
          "case_component_intersections_mm3": {}}
for case_name in ("cover", "back"):
    shape = parts[case_name].val()
    report["case_validity"][case_name] = {
        "valid": shape.isValid(),
        "solids": len(parts[case_name].solids().vals()),
    }
    for comp_name in ("display", "rtc", "xiao_pcb", "xiao_shield", "usb", "battery", "foam"):
        common = parts[case_name].intersect(parts[comp_name])
        volume = common.val().Volume() if common.val() else 0.0
        if volume > 0.01:
            report["case_component_intersections_mm3"][f"{case_name}/{comp_name}"] = round(volume, 4)
case_common = cover.intersect(back)
report["cover_back_intersection_mm3"] = round(case_common.val().Volume() if case_common.val() else 0.0, 6)
assert all(v["valid"] and v["solids"] == 1 for v in report["case_validity"].values()), report
assert not report["case_component_intersections_mm3"], report
assert report["cover_back_intersection_mm3"] < 0.01, report
(OUT / "v2_fit_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
print("saved v2_cover, v2_back, v2_assembly")
