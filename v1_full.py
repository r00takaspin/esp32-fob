#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FOB-1 v1.1 — корпус + начинка. Экспорт STEP/STL для печати и рендера.

Изменения v1.1 (после проверки пересечений):
- плата XIAO сдвинута вправо, край заподлицо с наружной гранью стенки (x=46):
  плата вдвигается через прорезь в стенке, разъём USB-C доступен без утопления;
  старая посадка (x 24..45) врезалась в стенку и в углы полости;
- радиус углов полости RC 3.5 → 1.8: RTC 42×17 и АКБ 20×11 не влезали
  в скруглённые углы (врезание до 1,45 мм);
- RTC сдвинут y 2.0 → 2.4 (зазор в углах), АКБ 1.5/1.5 → 2.4/2.0 (зазор до стенок);
- отверстие под провода кнопки перенесено: было x=31.8, z=8.45 — упиралось
  в модуль RTC; теперь x=18.0, z=11.0 — свободный канал между АКБ и платой;
- бортик крышки 0.5×0.8 в паз 0.8×1.3 (зазор 0,15 мм/сторону): было 0,5 в 0,5
  с нулевым зазором — после печати не собиралось;
- дисплей: 4 ребра фиксации вместо 2 (не было фиксации по x);
- убраны рёбра-полки над платой: они пересекали плату (61 мм³) и делали
  сборку невозможной; плату теперь держит прорезь в стенке;
- сборка: в перевёрнутый стакан — АКБ (на поролон), XIAO в прорезь,
  RTC, дисплей, крышка.
"""
import cadquery as cq
from cadquery import exporters

W, H, R = 46.0, 24.0, 5.0
T, T_FRONT = 17.0, 2.0
Z_CAV0, Z_CAV1 = 2.0, 14.4
WALL, RC = 1.5, 1.8
EAR_TIP_X, EAR_TAB_H, EAR_END_X = -4.6, 8.4, 2.0
HOLE_D, HOLE_Y = 3.6, 12.0
WIN_X, WIN_Y, WIN_W, WIN_H = 11.5, 8.8, 23.0, 6.4
DISP = (4.75, 5.75, 36.5, 12.5)      # OLED 0,91" 128×32
BRD = (25.0, 3.1, 21.0, 17.8)        # XIAO: правый край заподлицо со стенкой (x=46)
BAT = (2.4, 2.0, 11.0, 20.0)         # LiPo 401120: 20×11×4, лёжа
RTC = (2.0, 2.4, 42.0, 17.0)         # PCF8563 42×17×6
Z_BRD = 9.3                          # низ платы XIAO = верх RTC
# прорезь под плату в правой стенке и окно под штекер USB-C
SLIT_Y0, SLIT_Y1, SLIT_Z0, SLIT_Z1 = 3.0, 21.0, 9.15, 10.45
USB_Y0, USB_Y1, USB_Z0, USB_Z1 = 6.9, 17.1, 9.2, 13.4
# провода мембранной кнопки: отверстие выходит в свободный канал над RTC
BTN_HOLE_X, BTN_HOLE_Z, BTN_HOLE_D = 18.0, 11.0, 2.5

def body(z0, h):
    box = (cq.Workplane("XY").center(W/2, H/2).rect(W, H).extrude(h).edges("|Z").fillet(R))
    ear = (cq.Workplane("XY").slot2D((EAR_END_X-EAR_TIP_X)+EAR_TAB_H, EAR_TAB_H).extrude(h)
           .translate(((EAR_TIP_X+EAR_END_X)/2, HOLE_Y, 0)))
    return box.union(ear).translate((0,0,z0))

def cavity(z0, h):
    return (cq.Workplane("XY").center(WALL+(W-2*WALL)/2, H/2).rect(W-2*WALL, H-2*WALL)
            .extrude(h).edges("|Z").fillet(RC).translate((0,0,z0)))

def blk(x0,x1,y0,y1,z0,z1, r=0.0):
    w = (cq.Workplane("XY", origin=(0,0,z0)).center((x0+x1)/2,(y0+y1)/2)
         .rect(x1-x0,y1-y0).extrude(z1-z0))
    if r: w = w.edges("|Z").fillet(r)
    return w

def cyl_y(d, x, z, y0, y1):
    return (cq.Workplane("XY").circle(d/2).extrude(y1-y0)
            .rotate((0,0,0),(1,0,0),-90).translate((x, y0, z)))

def rrect(w,h,r,cx,cy,z0,hz):
    return (cq.Workplane("XY", origin=(0,0,z0)).center(cx,cy).rect(w,h).extrude(hz)
            .edges("|Z").fillet(r))

def hole(d,x,y,z0,h):
    return cq.Workplane("XY", origin=(0,0,z0)).center(x,y).circle(d/2).extrude(h)

def ring_lip(z0, h, inset, width):
    """Кольцо у стенки: бортик крышки (inset 1.0, width 0.5) или паз в стакане
    (inset 0.85, width 0.8) — зазор 0,15 мм на сторону."""
    o = (cq.Workplane("XY", origin=(0,0,z0)).center(W/2,H/2)
         .rect(W-2*inset, H-2*inset).extrude(h).edges("|Z").fillet(R-inset))
    i = (cq.Workplane("XY", origin=(0,0,z0)).center(W/2,H/2)
         .rect(W-2*(inset+width), H-2*(inset+width)).extrude(h)
         .edges("|Z").fillet(RC+(WALL-inset-width)))
    return o.cut(i)

# ---------------------------------------------------------------- крышка
cover = body(0, T_FRONT).edges("<Z").fillet(1.2)   # скруглить верхнюю кромку
cover = cover.cut(rrect(WIN_W, WIN_H, 0.6, WIN_X+WIN_W/2, WIN_Y+WIN_H/2, -1, T_FRONT+2))
cover = cover.cut(hole(HOLE_D, EAR_TIP_X, HOLE_Y, -1, T_FRONT+2))
dx,dy,dw,dh = DISP
for rb in (blk(dx,dx+dw,dy-0.6,dy,T_FRONT,T_FRONT+1.3),        # ребра фиксации дисплея,
           blk(dx,dx+dw,dy+dh,dy+dh+0.6,T_FRONT,T_FRONT+1.3),  # теперь с 4 сторон
           blk(dx-0.6,dx,dy,dy+dh,T_FRONT,T_FRONT+1.3),
           blk(dx+dw,dx+dw+0.6,dy,dy+dh,T_FRONT,T_FRONT+1.3)):
    cover = cover.union(rb)
cover = cover.union(ring_lip(T_FRONT, 0.8, 1.0, 0.5))  # бортик 0,5 × 0,8
cover = cover.cut(cyl_y(2.0, 34.0, T_FRONT, -0.5, 1.5))  # паз под ноготь

# ---------------------------------------------------------------- дно
back = body(Z_CAV0, T-Z_CAV0).edges(">Z").fillet(1.2)   # скруглить нижнюю кромку
back = back.cut(cavity(Z_CAV0, Z_CAV1-Z_CAV0))
back = back.cut(hole(HOLE_D, EAR_TIP_X, HOLE_Y, Z_CAV0-1, T))
# прорезь под плату (плата вдвигается сбоку) + окно под штекер USB-C
back = back.cut(blk(44.3, W+1.0, SLIT_Y0, SLIT_Y1, SLIT_Z0, SLIT_Z1))
back = back.cut(blk(44.3, W+1.0, USB_Y0, USB_Y1, USB_Z0, USB_Z1))
# провода мембранной кнопки: выходят в свободный канал между АКБ и платой
back = back.cut(cyl_y(BTN_HOLE_D, BTN_HOLE_X, BTN_HOLE_Z, -1.0, 2.6))
back = back.cut(ring_lip(Z_CAV0, 1.3, 0.85, 0.8))        # паз 0,8 × 1,3 под бортик
back = back.cut(cyl_y(2.0, 34.0, T_FRONT, -0.5, 1.5))    # паз под ноготь на стыке

# ---------------------------------------------------------------- начинка
display = blk(DISP[0], DISP[0]+DISP[2], DISP[1], DISP[1]+DISP[3], 2.0, 3.3, 1.0)
pcb = blk(BRD[0], BRD[0]+BRD[2], BRD[1], BRD[1]+BRD[3], 9.3, 10.3, 1.0)
shield = blk(29.0, 42.0, 5.5, 18.5, 10.3, 12.3, 0.8)
usb_c = blk(44.8, 46.6, 7.5, 16.5, 9.5, 12.5, 0.6)
batt = blk(BAT[0], BAT[0]+BAT[2], BAT[1], BAT[1]+BAT[3], 9.3, 13.3, 1.0)
rtc = blk(RTC[0], RTC[0]+RTC[2], RTC[1], RTC[1]+RTC[3], 3.3, 9.3, 0.6)
# ---------------------------------------------------------------- мембранная кнопка (покупная)
button = blk(19.5, 30.5, -1.2, 0.0, 5.0, 11.9)           # накладка 11×6,9 на стенке
button_center = cyl_y(4.0, 25.0, 8.45, -1.25, -1.0)      # цветной центр
wire = blk(17.6, 19.5, -0.95, -0.1, 10.5, 11.4).union(   # 2 провода вдоль стенки
       cyl_y(1.6, BTN_HOLE_X, BTN_HOLE_Z, -0.7, 2.2))    # и жгут сквозь отверстие
coin = cq.Workplane("XY").center(73.0, 12.5).circle(25.0/2).extrude(1.8)  # 5 ₽, масштаб

for nm, p in (("cover",cover),("back",back),("display",display),("pcb",pcb),
              ("shield",shield),("usbc",usb_c),("batt",batt),("rtc",rtc),
              ("button",button),("button_center",button_center),("wire",wire),
              ("coin",coin)):
    if nm in ("cover","back"):
        exporters.export(p, f"parts/v1_{nm}.step")
        exporters.export(p, f"parts/v1_{nm}.stl", tolerance=0.02, angularTolerance=0.15)
    else:
        exporters.export(p, f"/tmp/r_{nm}.stl", tolerance=0.05, angularTolerance=0.2)
print("ok")
