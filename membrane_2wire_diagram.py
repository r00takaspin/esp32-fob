#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Мембранная кнопка на 2 проводах: вид спереди + разрез."""
O=[]
def add(s): O.append(s)
def n(v):
    if abs(v-round(v))<1e-9: return str(int(round(v)))
    return ("%.1f"%v)
def txt(x,y,s,size=18,anchor="start",fill="#1b2430",weight="normal"):
    add('<text x="%s" y="%s" font-family="Helvetica,Arial,sans-serif" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'%(n(x),n(y),n(size),fill,anchor,weight,s))
def rect(x,y,w,h,fill,stroke="#1b2430",sw=2.5,r=0):
    add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/>'%(n(x),n(y),n(w),n(h),n(r),fill,stroke,n(sw)))
def circle(x,y,r,fill,stroke="#1b2430",sw=2.5):
    add('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>'%(n(x),n(y),n(r),fill,stroke,n(sw)))
def line(x1,y1,x2,y2,w=3,c="#1b2430",dash=None):
    d=' stroke-dasharray="%s"'%dash if dash else ""
    add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(n(x1),n(y1),n(x2),n(y2),c,n(w),d))
def arrow(x1,y1,x2,y2,c="#1b2430",w=3):
    import math
    line(x1,y1,x2,y2,w,c)
    a=math.atan2(y2-y1,x2-x1)
    for da in (2.7,-2.7):
        px=x2+14*math.cos(a+da); py=y2+14*math.sin(a+da)
        line(x2,y2,px,py,w,c)

W,H=1100,620
add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">'%(W,H))
add('''<defs><pattern id="h" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="10" stroke="#9aa5b1" stroke-width="1.3"/></pattern></defs>''')
rect(0,0,W,H,"#fcfbf7","#fcfbf7",0)
txt(40,48,"Мембранная кнопка на 2 проводах — вид спереди",30,"start","#1b2430","bold")
txt(40,80,"Клеится снаружи, провода уходят внутрь через отверстие",18,"start","#6b7682")

S=19.0
def X(x): return 80 + x*S
def Y(z): return 130 + z*S

# передняя стенка (вид снаружи): 41 x 12
rect(X(0),Y(0),41*S,12*S,"url(#h)","#1b2430",3,10)
# кнопка Ø7 (накладка)
circle(X(25),Y(5.5),3.5*S,"#2b2f36","#151a20",2.5)
circle(X(25),Y(5.5),2.0*S,"#3aa463","#1f6b3c",2.0)
txt(X(25),Y(5.5)+6,"ЗЕЛЁНАЯ",14,"middle","#ffffff","bold")
# отверстие Ø2,5
circle(X(29.5),Y(5.5),1.25*S,"#fcfbf7","#1b2430",2.2)
# 2 провода от кнопки к отверстию
line(X(28.4),Y(4.9),X(29.5),Y(4.9),5,"#c9a227")
line(X(28.4),Y(6.1),X(29.5),Y(6.1),5,"#c9a227")
# провода дальше внутрь (пунктир)
line(X(29.5),Y(4.9),X(35),Y(3.0),4,"#c9a227","6 4")
line(X(29.5),Y(6.1),X(35),Y(8.0),4,"#c9a227","6 4")

# подписи
arrow(X(25),Y(10.5),X(25),Y(7.2),"#1b2430",3)
txt(X(25),Y(11.2),"кнопка Ø7 — клеится снаружи",17,"middle","#1b2430","bold")

line(X(29.5),Y(5.5)-26,X(40),Y(1.0),2,"#1b2430","5 4")
txt(X(40),Y(1.0)-8,"отверстие Ø2,5",16,"start","#1b2430","bold")
txt(X(40),Y(1.0)+14,"под 2 провода",14,"start","#6b7682")

txt(X(35)+8,Y(3.0),"к D1 / GND",15,"start","#8a6d12","bold")

# ---- вставка: разрез ----
BX,BY=700,380
txt(BX,BY-14,"Разрез (как провод проходит сквозь стенку)",17,"start","#6b7682","bold")
# стенка
rect(BX,BY,26,90,"url(#h)","#1b2430",2.5)
# кнопка снаружи
rect(BX-24,BY+15,24,60,"#2b2f36","#151a20",2.5,4)
rect(BX-24,BY+30,24,30,"#3aa463","#1f6b3c",2.0,2)
# провода
line(BX-2,BY+35,BX+52,BY+35,5,"#c9a227")
line(BX-2,BY+55,BX+52,BY+55,5,"#c9a227")
txt(BX+56,BY+40,"D1",15,"start","#1b2430","bold")
txt(BX+56,BY+60,"GND",15,"start","#1b2430","bold")
txt(BX-30,BY+100,"снаружи",14,"start","#6b7682")
txt(BX+56,BY+100,"внутри",14,"start","#6b7682")

add('</svg>')
open("membrane_2wire_diagram.svg","w",encoding="utf-8").write("\n".join(O))
print("ok")
