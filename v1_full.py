#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FOB-1 v1 — корпус + начинка + плунжер. Экспорт STL для рендера."""
import cadquery as cq
from cadquery import exporters

W, H, R = 46.0, 24.0, 5.0
T, T_FRONT = 17.0, 2.0
Z_CAV0, Z_CAV1 = 2.0, 14.4
WALL, RC = 1.5, 3.5
EAR_TIP_X, EAR_TAB_H, EAR_END_X = -4.6, 8.4, 2.0
HOLE_D, HOLE_Y = 3.6, 12.0
WIN_X, WIN_Y, WIN_W, WIN_H = 11.5, 8.8, 23.0, 6.4
DISP = (4.75, 5.75, 36.5, 12.5)
BRD = (24.0, 3.1, 21.0, 17.8)
BAT = (1.5, 1.5, 11.0, 20.0)   # LiPo 401120: 20×11×4, лёжа (11 по x, 20 по y)
Z_BRD, Z_LIP = 9.3, 9.0
USB_Z0, USB_Z1, USB_Y0, USB_Y1 = 9.5, 12.5, 7.5, 16.5
BTN_X = 25.0                  # боковая кнопка: положение по x
MEM_D = 5.0                   # мембрана (покупается) Ø5,0 — целиком на стенке стакана
MEM_REC_D = 5.2               # цековка под мембрану Ø5,2
MEM_REC_T = 0.6               # глубина цековки, мм
PUSHER_D = 2.0                # толкатель мембраны
MEM_HOLE_D = 2.4              # сквозное отверстие под толкатель
SW_Y0, SW_Y1 = 2.5, 5.5       # корпус тактовой кнопки 3,5 × 3,0 × 1,75 (по y)
SW_Z0, SW_Z1 = 3.45, 5.2      # тактовая по z: сидит на верхней стороне платы
BTN_Z = 4.6                   # ось кнопки: чуть выше актуатора (4,325), чтобы мембрана целиком легла на стенку

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

def cyl(d,x,y,z0,z1):
    return cq.Workplane("XY", origin=(0,0,z0)).center(x,y).circle(d/2).extrude(z1-z0)

def cyl_y(d, x, z, y0, y1):
    return (cq.Workplane("XY").circle(d/2).extrude(y1-y0)
            .rotate((0,0,0),(1,0,0),-90).translate((x, y0, z)))

def rrect(w,h,r,cx,cy,z0,hz):
    return (cq.Workplane("XY", origin=(0,0,z0)).center(cx,cy).rect(w,h).extrude(hz)
            .edges("|Z").fillet(r))

def hole(d,x,y,z0,h):
    return cq.Workplane("XY", origin=(0,0,z0)).center(x,y).circle(d/2).extrude(h)

def ring_lip(z0, h):
    """Кольцо-бортик 0,5 мм у внутреннего края стенки (паз/бортик крышки)."""
    o = (cq.Workplane("XY", origin=(0,0,z0)).center(W/2,H/2).rect(W-2, H-2).extrude(h)
         .edges("|Z").fillet(R-0.5))
    i = (cq.Workplane("XY", origin=(0,0,z0)).center(W/2,H/2).rect(W-2*WALL, H-2*WALL).extrude(h)
         .edges("|Z").fillet(RC))
    return o.cut(i)

# ---------------------------------------------------------------- крышка
cover = body(0, T_FRONT).edges("<Z").fillet(1.2)   # скруглить верхнюю кромку
cover = cover.cut(rrect(WIN_W, WIN_H, 0.6, WIN_X+WIN_W/2, WIN_Y+WIN_H/2, -1, T_FRONT+2))
cover = cover.cut(hole(HOLE_D, EAR_TIP_X, HOLE_Y, -1, T_FRONT+2))
dx,dy,dw,dh = DISP
cover = cover.union(blk(dx,dx+dw,dy-0.6,dy,T_FRONT,T_FRONT+1.3))
cover = cover.union(blk(dx,dx+dw,dy+dh,dy+dh+0.6,T_FRONT,T_FRONT+1.3))
cover = cover.union(ring_lip(T_FRONT, 1.0))   # бортик для съёмной крышки
cover = cover.cut(cyl_y(2.0, 34.0, T_FRONT, -0.5, 1.5))  # паз под ноготь

# ---------------------------------------------------------------- дно
back = body(Z_CAV0, T-Z_CAV0).edges(">Z").fillet(1.2)   # скруглить нижнюю кромку
back = back.cut(cavity(Z_CAV0, Z_CAV1-Z_CAV0))
back = back.cut(hole(HOLE_D, EAR_TIP_X, HOLE_Y, Z_CAV0-1, T))
back = back.cut(blk(44.5, W+1.0, USB_Y0, USB_Y1, USB_Z0, USB_Z1))
bx,by,bw,bh = BRD
for m in (blk(bx, W-WALL, by, by+1.5, Z_BRD, Z_CAV1),
          blk(bx, W-WALL, by+bh-1.5, by+bh, Z_BRD, Z_CAV1),
          blk(bx, W-WALL, by-0.6, by, Z_LIP, Z_CAV1),
          blk(bx, W-WALL, by+bh, by+bh+0.6, Z_LIP, Z_CAV1),
          blk(bx-1.5, bx, WALL, H-WALL, Z_LIP, Z_CAV1)):
    back = back.union(m)
# мембранная кнопка на 2 проводах: плоская площадка снаружи + отверстие под провода
back = back.cut(cyl_y(2.5, 31.8, 8.45, -1.0, 2.6))   # отверстие под провода Ø2,5
back = back.cut(ring_lip(Z_CAV0, 1.0))                # паз под бортик крышки
back = back.cut(cyl_y(2.0, 34.0, T_FRONT, -0.5, 1.5)) # паз под ноготь на стыке

# ---------------------------------------------------------------- начинка
display = blk(DISP[0], DISP[0]+DISP[2], DISP[1], DISP[1]+DISP[3], 2.0, 3.3, 1.0)
pcb = blk(BRD[0], BRD[0]+BRD[2], BRD[1], BRD[1]+BRD[3], 9.3, 10.3, 1.0)
shield = blk(28.0, 41.0, 5.5, 18.5, 10.3, 12.3, 0.8)
usb_c = blk(44.0, 46.5, 7.5, 16.5, 9.5, 12.5, 0.6)
batt = blk(BAT[0], BAT[0]+BAT[2], BAT[1], BAT[1]+BAT[3], 9.3, 13.3, 1.0)
# готовый модуль RTC HW-689 30×20×7 — отдельный слой над АКБ и XIAO
rtc = blk(2.0, 44.0, 2.0, 19.0, 3.3, 9.3, 0.6)   # PCF8563 42×17×6
# ---------------------------------------------------------------- мембранная кнопка на 2 проводах (покупается)
button = blk(19.5, 30.5, -1.2, 0.0, 5.0, 11.9)           # накладка 11×6,9 на стенке
button_center = cyl_y(4.0, 25.0, 8.45, -1.25, -1.0)     # цветной центр
wire = blk(30.4, 32.2, -0.7, 2.4, 7.9, 9.0)              # 2 провода через отверстие

for nm, p in (("cover",cover),("back",back),("display",display),("pcb",pcb),
              ("shield",shield),("usbc",usb_c),("batt",batt),("rtc",rtc),
              ("button",button),("button_center",button_center),("wire",wire)):
    if nm in ("cover","back"):
        exporters.export(p, f"parts/v1_{nm}.step")
        exporters.export(p, f"parts/v1_{nm}.stl", tolerance=0.02, angularTolerance=0.15)
    else:
        exporters.export(p, f"/tmp/r_{nm}.stl", tolerance=0.05, angularTolerance=0.2)
print("ok")
