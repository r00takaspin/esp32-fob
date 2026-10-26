#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FOB-1 v1 — схема пайки и компоновка. Лист A4, мм."""
import math
O = []
def add(s): O.append(s)
def n(v):
    if abs(v - round(v)) < 1e-9: return str(int(round(v)))
    return ("%.3f" % v).rstrip("0").rstrip(".")
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

INK="#1b2430"; SOFT="#8b98a8"; PAPER="#fcfbf7"; WHITE="#ffffff"
RED="#c0392b"; BLK="#2d3436"; BLU="#1f6fb2"; GRN="#2e8b57"; ORA="#c77b1e"; TAN="#d8c9b2"

def line(x1,y1,x2,y2,w=0.35,c=INK,dash=None,cap="round"):
    d=' stroke-dasharray="%s"'%dash if dash else ""
    add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s stroke-linecap="%s"/>'
        %(n(x1),n(y1),n(x2),n(y2),c,n(w),d,cap))
def poly(pts,w=0.35,c=INK,fill="none",dash=None,cap="round",join="round"):
    d=" ".join(("%s,%s")%(n(a),n(b)) for a,b in pts)
    dd=' stroke-dasharray="%s"'%dash if dash else ""
    add('<polyline points="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linecap="%s" stroke-linejoin="%s"/>'
        %(d,fill,c,n(w),dd,cap,join))
def box(x,y,w,h,r=1.6,fill=WHITE,sw=0.35,c=INK,dash=None):
    d=("M %s,%s H %s A %s,%s 0 0 1 %s,%s V %s A %s,%s 0 0 1 %s,%s H %s A %s,%s 0 0 1 %s,%s V %s A %s,%s 0 0 1 %s,%s Z"
       %(n(x+r),n(y),n(x+w-r),n(r),n(r),n(x+w),n(y+r),n(y+h-r),n(r),n(r),n(x+w-r),n(y+h),
         n(x+r),n(r),n(r),n(x),n(y+h-r),n(y+r),n(r),n(r),n(x+r),n(y)))
    dd=' stroke-dasharray="%s"'%dash if dash else ""
    add('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'%(d,fill,c,n(sw),dd))
def txt(x,y,s,size=2.2,anchor="start",fill=INK,font="Helvetica",weight="normal",rot=0,ls=0):
    t='<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s"'%(
        n(x),n(y),font,n(size),fill,anchor,weight)
    if rot: t+=' transform="rotate(%s %s %s)"'%(n(rot),n(x),n(y))
    if ls: t+=' letter-spacing="%s"'%n(ls)
    add(t+">%s</text>"%esc(s))
def dot(x,y,c=INK,r=0.5):
    add('<circle cx="%s" cy="%s" r="%s" fill="%s"/>'%(n(x),n(y),n(r),c))
def pin(x,y,label,side="r",c=INK):
    add('<circle cx="%s" cy="%s" r="0.75" fill="%s" stroke="%s" stroke-width="0.18"/>'%(n(x),n(y),WHITE,c))
    if side=="r": txt(x-2.6,y+0.8,label,1.85,"end",INK)
    else:         txt(x+2.6,y+0.8,label,1.85,"start",INK)

W,H=297.,210.
add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" viewBox="0 0 %s %s">'%(n(W),n(H),n(W),n(H)))
add("""<defs>
<pattern id="h" width="1.3" height="1.3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="1.3" stroke="#1b2430" stroke-width="0.1"/></pattern>
</defs>""")
add('<rect width="%s" height="%s" fill="%s"/>'%(n(W),n(H),PAPER))
add('<rect x="8" y="8" width="%s" height="%s" fill="none" stroke="%s" stroke-width="0.4"/>'%(n(W-16),n(H-16),INK))

# ---------- шапка ----------
txt(14,20,"FOB-1 v1",5.2,"start",INK,"Helvetica","bold",ls=0.4)
txt(52,18.4,"схема пайки и компоновка",3.0,"start",INK)
txt(52,22.8,"XIAO ESP32-C3 + OLED 0,91\" + PCF8563 + кнопка · корпус 41 × 24 × 17 мм · 12 точек",2.0,"start",SOFT)
line(12,27.5,285,27.5,0.3,INK)

# ---------- зона A: схема соединений ----------
txt(14,34.5,"1. СОЕДИНЕНИЯ",2.1,"start",INK,"Helvetica","bold",ls=0.6)
txt(14,38.2,"пересечения без точек — не соединены",1.7,"start",SOFT)

# XIAO
box(25,55,40,42,fill="#eef2f7")
txt(45,72,"XIAO",2.6,"middle",INK,"Helvetica","bold")
txt(45,76,"ESP32-C3",2.0,"middle",INK)
txt(45,79.5,"USB-C →",1.7,"middle",SOFT)
pin(65,60,"3V3","r"); pin(65,68,"GND","r"); pin(65,76,"D4","r"); pin(65,84,"D5","r")
pin(65,92,"D1","r")
pin(25,66,"BAT+","l"); pin(25,78,"BAT−","l")

# дисплей
box(118,42,50,34,fill="#eef2f7")
txt(143,56,"OLED 0,91\"",2.4,"middle",INK,"Helvetica","bold")
txt(143,60,"128×32 · 0x3C",1.9,"middle",SOFT)
pin(118,48,"VCC","l"); pin(118,54,"GND","l"); pin(118,60,"SDA","l"); pin(118,66,"SCL","l")
txt(118,80.5,"порядок пинов сверь с шелкографией на своей плате",1.55,"start",ORA)

# RTC
box(118,88,50,32,fill="#eef2f7")
txt(143,102,"PCF8563",2.4,"middle",INK,"Helvetica","bold")
txt(143,106,"RTC · 0x51",1.9,"middle",SOFT)
pin(118,94,"VDD","l"); pin(118,100,"GND","l"); pin(118,106,"SDA","l"); pin(118,112,"SCL","l")

# батарея
box(10,124,32,18,r=2.5,fill="#f3ead9")
txt(26,134.5,"LiPo 3,7 В",1.9,"middle",INK)
txt(26,138.3,"100 мА·ч",1.8,"middle",SOFT)
add('<circle cx="24" cy="124" r="0.75" fill="%s" stroke="%s" stroke-width="0.18"/>'%(WHITE,RED))
add('<circle cx="34" cy="124" r="0.75" fill="%s" stroke="%s" stroke-width="0.18"/>'%(WHITE,BLK))
txt(25.4,128.6,"+",1.9,"start",RED,"Helvetica","bold")
txt(35.4,128.6,"−",1.9,"start",BLK,"Helvetica","bold")

# провода: 4 шины
NETS=[("3V3",RED,60,88,48,94),("GND",BLK,68,94,54,100),
      ("SDA",BLU,76,101,60,106),("SCL",GRN,84,108,66,112)]
for name,c,y0,xl,yd,yr in NETS:
    poly([(65,y0),(xl,y0),(xl,yd),(118,yd)],0.6,c)         # к дисплею
    poly([(xl,y0),(xl,yr),(118,yr)],0.6,c)                  # к RTC
    dot(xl,y0,c,0.6)
    txt(xl-1.2,y0-1.6,name,1.7,"end",c,"Helvetica","bold")

# батарея
poly([(25,66),(20,66),(20,120),(24,120),(24,124)],0.6,RED)
poly([(25,78),(15,78),(15,118),(34,118),(34,124)],0.6,BLK)

# своя кнопка
box(72,104,44,18,fill="#f3ead9")
txt(94,111,"КНОПКА",2.0,"middle",INK,"Helvetica","bold")
txt(94,115.2,"мембранная · 2 провода",1.55,"middle",SOFT)
pin(72,108,"D1","l",ORA); pin(72,115,"GND","l",ORA)
poly([(65,92),(69,92),(69,108),(72,108)],0.6,ORA)
poly([(65,68),(67,68),(67,115),(72,115)],0.6,BLK)
dot(65,92,ORA,0.6)

# ---------- зона B: компоновка ----------
txt(176,34.5,"2. КОМПОНОВКА",2.1,"start",INK,"Helvetica","bold",ls=0.6)
S=2.0; BX,BY=186.,42.
def L(x,y): return (BX+x*S, BY+y*S)
# контур: капсула 42 обрезана на 40,5
add('<g transform="translate(%s,%s) scale(%s)">'%(n(BX),n(BY),n(S)))
add('<path d="M 5,0 L 36,0 A 5,5 0 0 1 41,5 L 41,17 A 5,5 0 0 1 36,22 L 5,22 A 5,5 0 0 1 0,17 L 0,15.2 L -4.6,15.2 A 4.2,4.2 0 0 1 -4.6,6.8 L 0,6.8 L 0,5 A 5,5 0 0 1 5,0 Z" fill="#f6f8fa" stroke="%s" stroke-width="0.5"/>'%INK)
add('<rect x="38.4" y="7.4" width="2.1" height="7.2" rx="0.8" fill="#20262e"/>')
add('<g transform="translate(0,0)">')
add('<circle cx="25" cy="0.75" r="3.25" fill="#dbe4ee" stroke="%s" stroke-width="0.45"/>'%INK)
add('<circle cx="25" cy="0.75" r="2.1" fill="none" stroke="%s" stroke-width="0.25"/>'%SOFT)
def rr2(x,y,w,h,r,fill,stroke,dash=None,wid=0.35):
    dd=' stroke-dasharray="%s"'%dash if dash else ""
    add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
        %(n(x),n(y),n(w),n(h),n(r),fill,stroke,n(wid),dd))
rr2(18,3.1,21,17.8,1.2,"#dbe4ee",INK,None,0.45)      # XIAO
rr2(1.5,1.5,11,20,1.0,"#f0e3cc",INK,None,0.45)           # АКБ
rr2(2,2,30,20,1.0,"#cfe0f0",BLU,"1.2 0.9",0.4)    # RTC сверху
rr2(2,5.75,36.5,12.5,1.0,"none",SOFT,"1.6 1.1",0.4)  # дисплей сверху
add('</g>')
txt(28.5,12.5,"XIAO",2.2,"middle",INK,"Helvetica","bold")
txt(9.5,21.5,"АКБ",2.0,"middle",INK,"Helvetica","bold")
txt(9.5,6.5,"RTC",1.8,"middle",BLU,"Helvetica","bold")

add('</g>')
txt(BX,BY-2.5,"вид сверху · пунктиром — дисплей, лежит на крышке",1.7,"start",SOFT)

# разрез
CX,CY,SS=186.,104.,1.7
add('<g transform="translate(%s,%s) scale(%s)">'%(n(CX),n(CY),n(SS)))
def band(x0,x1,z0,z1,fill,stroke=INK,wid=0.4,label=None):
    add('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
        %(n(x0),n(z0),n(x1-x0),n(z1-z0),fill,stroke,n(wid)))
band(0,41,0,2.0,"url(#h)")                 # крышка
band(2.2,37.8,2.0,3.3,"#1b2530")             # дисплей
band(2.0,32.0,3.3,10.3,"#cfe0f0")            # RTC 30×20×7
band(1.5,12.5,10.3,14.3,TAN)                  # АКБ
band(18.5,39.0,10.3,13.3,"#dbe4ee")           # XIAO
band(0,1.5,2.0,14.4,"url(#h)")                # стенка
band(39.5,41,2.0,14.4,"url(#h)")            # стенка
band(0,41,14.4,17.0,"url(#h)")              # дно
add('</g>')
txt(CX,CY-3,"разрез по оси, масштаб 2:1",1.7,"start",SOFT)
txt(176,138,"Корпус 41 × 24 × 17 мм. RTC HW-689 30 × 20 × 7 — отдельным слоем над АКБ.",1.65,"start",SOFT)
txt(176,141.6,"В v2 RTC уедет на общую плату — корпус вернётся к 10–11 мм.",1.65,"start",SOFT)
txt(CX+71,CY+8,"17,0",2.0,"end",SOFT)
line(CX+72,CY,CX+72,CY+17.0*SS,0.2,SOFT)
line(CX+70,CY,CX+74,CY,0.2,SOFT); line(CX+70,CY+17.0*SS,CX+74,CY+17.0*SS,0.2,SOFT)

# ---------- зона C: шаги ----------
line(12,150,285,150,0.25,INK)
txt(14,157,"3. ПОШАГОВО",2.1,"start",INK,"Helvetica","bold",ls=0.6)
STEPS=[
 ("1","Прошей XIAO. USB-C в комп, Arduino IDE, blink."),
 ("2","Проверь I2C: дисплей и RTC на макетку, сканер должен увидеть 0x3C и 0x51."),
 ("3","Припаяй 4 провода к дисплею: VCC, GND, SDA, SCL. Длина 60 мм, провод 0,2 мм²."),
 ("4","Припаяй 4 провода к плате RTC. Длина 40 мм — она ляжет сверху на АКБ."),
 ("5","Собери шину: 3V3 → VCC/VDD, GND → GND/GND, D4 → SDA, D5 → SCL."),
 ("6","Кнопка: 2 провода на D1 и GND. Провода заведи в отверстие Ø2,5, мембрану приклей снаружи."),
 ("7","Проверь на столе от АКБ, USB отключён. Код должен совпасть с телефоном."),
 ("8","АКБ: красный на BAT+, чёрный на BAT−. Полярность перепутаешь — плата умрёт."),
 ("9","Первый заряд — под присмотром: 380 мА для банки 100 мА·ч это 3,8C."),
 ("10","Уложи: дисплей на крышку, XIAO справа, АКБ слева, RTC сверху на АКБ."),
 ("11","Приклей мембрану снаружи, провода в отверстие Ø2,5, закрой корпус."),
]
col_x=[14,106,198]
for i,(num,txt_s) in enumerate(STEPS):
    col=i//4; row=i%4
    x=col_x[col]; y=164+row*10.0
    add('<circle cx="%s" cy="%s" r="3.0" fill="%s"/>'%(n(x+2),n(y-1),INK))
    txt(x+2,y+0.1,num,2.3,"middle",WHITE,"Helvetica","bold")
    # перенос по строкам вручную
    words=txt_s.split(); ln=""; lines=[]; maxw=46
    for wd in words:
        if len(ln)+len(wd)+1<=maxw: ln=(ln+" "+wd).strip()
        else: lines.append(ln); ln=wd
    lines.append(ln)
    for j,l in enumerate(lines[:2]):
        txt(x+7,y+0.1+j*3.4,l,1.75,"start",INK)

add("</svg>")
open("FOB-1_payka.svg","w",encoding="utf-8").write("\n".join(O))
print("ok")
