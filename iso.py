#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FOB-1 v1 — изометрия сборки (разнесённый вид)."""
import math
O=[]; 
def add(s): O.append(s)
def n(v):
    if abs(v-round(v))<1e-9: return str(int(round(v)))
    return ("%.3f"%v).rstrip("0").rstrip(".")
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

INK="#1b2430"; SOFT="#8b98a8"; PAPER="#fcfbf7"; WHITE="#ffffff"; ACC="#2b6b86"
FILL="#e7ecf2"; XIAO="#2f6b52"; DISP="#1b2530"; PCB="#2f6b52"; BAT="#d8c9b2"; RTC="#3b6fa0"

def txt(x,y,s,size=2.2,anchor="start",fill=INK,font="Helvetica",weight="normal",ls=0):
    t=('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s"'
       %(n(x),n(y),font,n(size),fill,anchor,weight))
    if ls: t+=' letter-spacing="%s"'%n(ls)
    add(t+">%s</text>"%esc(s))
def line(x1,y1,x2,y2,w=0.3,c=INK,dash=None):
    d=' stroke-dasharray="%s"'%dash if dash else ""
    add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'
        %(n(x1),n(y1),n(x2),n(y2),c,n(w),d))
def path(d,w=0.3,c=INK,fill="none",rule=None):
    r=' fill-rule="%s"'%rule if rule else ""
    add('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>'%(d,fill,c,n(w),r))
def rr(x,y,w,h,r):
    return ("M %s,%s H %s A %s,%s 0 0 1 %s,%s V %s A %s,%s 0 0 1 %s,%s H %s A %s,%s 0 0 1 %s,%s V %s A %s,%s 0 0 1 %s,%s Z"
            %(n(x+r),n(y),n(x+w-r),n(r),n(r),n(x+w),n(y+r),n(y+h-r),n(r),n(r),n(x+w-r),n(y+h),
              n(x+r),n(r),n(r),n(x),n(y+h-r),n(y+r),n(r),n(r),n(x+r),n(y)))
def balloon(x,y,s,r=2.4,c=ACC):
    add('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="0.2"/>'%(n(x),n(y),n(r),WHITE,c))
    txt(x,y+0.85,s,2.2,"middle",c,"Helvetica","bold")

# --- силуэт корпуса v1: капсула 42, срез на 40.5, проушина ---
EX=0.833
BODY=("M 5,0 L 41,0 A 5,5 0 0 1 46,5 L 46,19 A 5,5 0 0 1 41,24 L 5,24 A 5,5 0 0 1 0,19 L 0,16.2 L -4.6,16.2 A 4.2,4.2 0 0 1 -4.6,7.8 L 0,7.8 L 0,5 A 5,5 0 0 1 5,0 Z")

W,H=297.,210.
add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" viewBox="0 0 %s %s">'%(n(W),n(H),n(W),n(H)))
add('<rect width="%s" height="%s" fill="%s"/>'%(n(W),n(H),PAPER))
add('<rect x="8" y="8" width="%s" height="%s" fill="none" stroke="%s" stroke-width="0.4"/>'%(n(W-16),n(H-16),INK))

txt(14,20,"FOB-1 v1",5.2,"start",INK,"Helvetica","bold",ls=0.4)
txt(52,18.4,"сборка · разнесённый вид",3.0,"start",INK)
txt(52,22.8,"крышка → дисплей → RTC → XIAO + АКБ → дно → кнопка на стенке · 46 × 24 × 17 мм",2.0,"start",SOFT)
line(12,27.5,285,27.5,0.3,INK)

IX,IY=88.,32.
K=0.86
MAT="matrix(%s,%s,%s,%s,0,0)"%(n(0.866*K),n(0.5*K),n(-0.866*K),n(0.5*K))

def layer(dy, art, thick):
    t=max(0.9,thick*0.6)
    add('<g transform="translate(%s,%s) %s">'%(n(IX),n(IY+dy+t),MAT)); art(True);  add('</g>')
    add('<g transform="translate(%s,%s) %s">'%(n(IX),n(IY+dy),MAT));   art(False); add('</g>')

def a_cover(dark):
    path(BODY+" "+rr(11.5,8.8,23,6.4,0.55),0.3,INK,"#aab4c1" if dark else FILL,rule="evenodd")
def a_disp(dark):
    path(rr(2,4.75,36.5,12.5,1.0),0.28,INK,"#0d131a" if dark else DISP)
    if not dark:
        path(rr(9,7.9,23,6.2,0.5),0.12,"#0a0e13","#0a0e13")
        path(rr(9.4,8.3,21.2,5.4,0.4),0.1,"#2b3c4a","none")
def a_rtc(dark):
    path(rr(2,2.4,42,17,0.8),0.28,INK,"#2c5580" if dark else RTC)
    if not dark:
        path(rr(5,4.5,7,5,0.4),0.14,"#111820","#0b0f14")
        path(rr(5.4,4.9,2.2,1.4,0.2),0.1,"#8a8f96","#6b7076")
def a_xiao(dark):
    path(rr(25,3.1,21,17.8,1.0),0.28,INK,"#22503d" if dark else XIAO)
    if not dark:
        path(rr(21.5,2.5,13,12,0.8),0.14,"#9aa3ac","#7d868f")
        path(rr(34.2,6.4,4.6,9.2,0.7),0.2,"#20262e","#151a20")
        path(rr(20.2,2.0,3.4,2.6,0.4),0.1,"#c9a227","#8d7220")
def a_bat(dark):
    path(rr(2.4,2.0,11,20,1.0),0.28,INK,"#8d8274" if dark else BAT)
    if not dark:
        path(rr(4.4,4.0,7.0,16.0,0.8),0.1,"#a89578","none")
        path("M 13.4,12 Q 15.9,12 15.9,15",0.5,"#b03a2e")
        path("M 13.4,6 Q 15.9,6 15.9,3",0.5,"#20262e")
CAV=rr(1.5,1.5,43,21,1.8)
def a_back(dark):
    path(BODY,0.3,INK,"#8f9aa7" if dark else FILL)
    if not dark:
        path(CAV,0.22,"#7d8894","#9aa5b1")                      # открытая полость
        path(rr(44.3,3.0,1.7,18.0,0.2),0.14,"#6f7a86","#3a424b")  # прорезь под плату
        path(rr(44.3,6.9,1.7,10.2,0.3),0.14,"#3a424b","#20262e")  # окно USB-C
        path(rr(16.75,-1.25,2.5,2.5,1.25),0.16,INK,"#8d97a3")  # отверстие под провода

def a_btn(dark):
    # накладка мембранной кнопки (как на фото): панель 11×7, зелёный центр, 2 провода
    path(rr(19.5,-2.0,11.0,7.0,1.2),0.28,INK,"#1f2328" if dark else "#2b2f36")
    if not dark:
        path(rr(22.5,-0.4,4.0,4.0,2.0),0.2,"#1f6b3c","#3aa463")
        path("M 30.5,0.5 L 34.5,0.5",0.5,"#c9a227")
        path("M 30.5,2.5 L 34.5,2.5",0.5,"#c9a227")

LAYERS=[
 (  0.0, a_cover, 2.0, "1", (41.3, 11.0)),
 ( 34.0, a_disp,  1.3, "2", (39.0, 10.6)),
 ( 54.0, a_rtc,   2.6, "3", (17.6, 4.6)),
 ( 71.0, a_xiao,  4.2, "4", (41.2, 8.2)),
 ( 87.0, a_bat,   3.5, None, None),
 (100.0, a_back,  2.6, "5", (41.3, 12.2)),
 (128.0, a_btn,   2.5, "6", (25.0, 0.3)),
]
for dy,art,th,num,anc in reversed(LAYERS):
    layer(dy,art,th)
for dy,art,th,num,anc in LAYERS:
    if num:
        bx,by=anc
        balloon(IX+0.866*K*(bx-by), IY+dy+0.5*K*(bx+by), num, r=2.4)

# --- подписи справа ---
txt(160,37,"СБОРКА СНИЗУ ВВЕРХ",1.8,"start",SOFT,"Helvetica","bold",ls=0.5)
txt(160,41.6,"слои 5 → 4 → 3 → 2 → 1 · кнопка 6 клеится на стенку",1.9,"start",SOFT)
line(160,45,250,45,0.2,SOFT)

CAPS=[
 ("1","КРЫШКА","пластина 2,0 · окно 23 × 6,4 · бортик 0,5 · съёмная",54),
 ("2","ДИСПЛЕЙ","36,5 × 12,5 · карман из 4 рёбер на крышке",82),
 ("3","RTC","PCF8563 42 × 17 · между дисплеем и платой",100),
 ("4","XIAO + АКБ","21 × 17,8 и 20 × 11 · плата в прорези стенки",118),
 ("5","ДНО-СТАКАН","стенка 1,5 · дно 2,6 · прорезь под плату + окно USB-C",140),
 ("6","КНОПКА","мембранная, 2 провода · D1/GND · клеится снаружи",160),
]
for num,name,sub,y in CAPS:
    balloon(160,y-0.8,num,r=2.4)
    txt(167,y,name,2.6,"start",INK,"Helvetica","bold",ls=0.4)
    txt(167,y+4.6,sub,1.9,"start",SOFT)

line(160,172,285,172,0.25,INK)
txt(160,178,"Сборка — в перевёрнутый стакан: АКБ (на поролон), XIAO правым",1.8,"start",INK)
txt(160,182.4,"краем в прорезь стенки, затем RTC, дисплей — в карман крышки.",1.8,"start",INK)
txt(160,186.8,"Мембрана снаружи, провода в отверстие Ø2,5; крышка — съёмная.",1.7,"start",INK)
txt(160,194,"Полость 43 × 21 × 12,4 мм · стенка 1,5 мм · 12 точек пайки",1.7,"start",SOFT)

add("</svg>")
open("FOB-1_assembly_iso.svg","w",encoding="utf-8").write("\n".join(O))
print("ok")
