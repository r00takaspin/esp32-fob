#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Схема пайки тонкого RTC: PCF8563T (SO-8) + кварц + обвязка."""
O=[]
def add(s): O.append(s)
def n(v):
    if abs(v-round(v))<1e-9: return str(int(round(v)))
    return ("%.1f"%v)
def txt(x,y,s,size=18,anchor="start",fill="#1b2430",weight="normal"):
    add('<text x="%s" y="%s" font-family="Helvetica,Arial,sans-serif" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'%(n(x),n(y),n(size),fill,anchor,weight,s))
def line(x1,y1,x2,y2,w=2.5,c="#1b2430"):
    add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>'%(n(x1),n(y1),n(x2),n(y2),c,n(w)))
def rect(x,y,w,h,fill="#ffffff",stroke="#1b2430",sw=2.5,r=0):
    add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/>'%(n(x),n(y),n(w),n(h),n(r),fill,stroke,n(sw)))
def dot(x,y,r=4):
    add('<circle cx="%s" cy="%s" r="%s" fill="#1b2430"/>'%(n(x),n(y),n(r)))
def p3v3(x,y):
    line(x,y,x,y-22,2.5,"#c0392b"); line(x-14,y-22,x+14,y-22,3,"#c0392b")
    txt(x,y-28,"3V3",13,"middle","#c0392b","bold")
def pgnd(x,y):
    line(x,y,x,y+22,2.5,"#1b2430")
    line(x-16,y+22,x+16,y+22,3,"#1b2430")
    line(x-9,y+29,x+9,y+29,2.2,"#1b2430")
    line(x-3,y+36,x+3,y+36,1.6,"#1b2430")

W,H=1250,760
add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">'%(W,H))
rect(0,0,W,H,"#fcfbf7","#fcfbf7",0)
txt(40,48,"Тонкий RTC: PCF8563T + кварц 32,768 кГц",30,"start","#1b2430","bold")
txt(40,78,"SO-8 · кварц 3215 · 2 конденсатора кварца 15 пФ · 2 подтяжки 10 кОм · конденсатор 100 нФ",16,"start","#6b7682")

# ---- чип ----
rect(500,190,190,340,"#eef2f6","#1b2430",3,8)
txt(595,350,"PCF8563T",18,"middle","#1b2430","bold")
txt(595,373,"SO-8",14,"middle","#6b7682")
for num,name,y in [("1","OSCI",250),("2","OSCO",330),("3","VSS",410),("4","VDD",490)]:
    line(440,y,500,y); txt(432,y+5,num,13,"end","#6b7682"); txt(508,y+5,name,14,"start","#1b2430")
for num,name,y in [("8","INT",250),("7","CLKOUT",330),("6","SCL",410),("5","SDA",490)]:
    line(690,y,750,y); txt(698,y+5,num,13,"start","#6b7682"); txt(682,y+5,name,14,"end","#1b2430")

# ---- кварц ----
line(440,250,380,250); line(380,250,380,278)
line(440,330,380,330); line(380,330,380,302)
rect(300,278,80,24,"#fff","#1b2430",2.5,5)
txt(340,295,"Y1 32,768",10,"middle","#1b2430","bold")

# ---- C1 / C2 ----
line(380,250,240,250); line(240,250,240,360)
line(220,360,260,360); line(220,378,260,378)
txt(212,354,"C1",13,"end","#1b2430","bold"); txt(212,375,"15 пФ",10,"end","#6b7682")
line(240,378,240,400); pgnd(240,400)
line(380,330,200,330); line(200,330,200,450)
line(180,450,220,450); line(180,468,220,468)
txt(172,444,"C2",13,"end","#1b2430","bold"); txt(172,465,"15 пФ",10,"end","#6b7682")
line(200,468,200,490); pgnd(200,490)

# ---- VSS ----
line(440,410,420,410); line(420,410,420,440); pgnd(420,440)
# ---- VDD + C3 ----
line(440,490,420,490); line(420,490,420,470); p3v3(420,470)
line(420,490,390,490); line(390,490,390,560)
line(370,560,410,560); line(370,578,410,578)
txt(362,554,"C3",13,"end","#1b2430","bold"); txt(362,575,"100 нФ",10,"end","#6b7682")
line(390,578,390,600); pgnd(390,600)

# ---- подтяжки ----
# R1 на SDA
line(750,490,980,490); line(830,490,830,470)
rect(817,420,26,50,"#fff","#1b2430",2.5,3)
txt(808,438,"R1",12,"end","#1b2430","bold"); txt(808,456,"10 кОм",9,"end","#6b7682")
line(830,420,830,400); p3v3(830,400); dot(830,490)
# R2 на SCL
line(750,410,980,410); line(890,410,890,390)
rect(877,340,26,50,"#fff","#1b2430",2.5,3)
txt(910,358,"R2",12,"start","#1b2430","bold"); txt(910,376,"10 кОм",9,"start","#6b7682")
line(890,340,890,310); p3v3(890,310); dot(890,410)

# ---- XIAO ----
rect(1010,220,200,380,"#eef2f6","#1b2430",3,10)
txt(1110,330,"XIAO",18,"middle","#1b2430","bold")
txt(1110,353,"ESP32-C3",12,"middle","#6b7682")
line(980,490,1010,490); line(980,410,1010,410)
txt(1030,510,"D4",13,"start","#1b2430"); txt(1030,432,"D5",13,"start","#1b2430")
txt(1005,478,"SDA",11,"start","#6b7682"); txt(1005,398,"SCL",11,"start","#6b7682")

# NC
line(750,250,830,250); txt(840,256,"NC",13,"start","#8b98a8")
line(750,330,860,330); txt(870,336,"NC",13,"start","#8b98a8")

# итог
txt(40,690,"Пайка: 8 выводов чипа + кварц + C1/C2 (15 пФ) + R1/R2 (10 кОм) + C3 (100 нФ).",14,"start","#1b2430")
txt(40,712,"VDD→3V3, VSS→GND, SDA→D4, SCL→D5. INT и CLKOUT — не подключаем. Резервную батарейку можно не ставить.",13,"start","#6b7682")

add('</svg>')
open("FOB-1_thin_rtc.svg","w",encoding="utf-8").write("\n".join(O))
print("ok")
