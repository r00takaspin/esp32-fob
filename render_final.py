#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FOB-1 — аккуратный 3/4-рендер из настоящих STL (суперсэмплинг)."""
import numpy as np, struct
from PIL import Image

def load(p):
    d=open(p,"rb").read(); n=struct.unpack("<I",d[80:84])[0]
    a=np.frombuffer(d,dtype=np.uint8,offset=84,count=n*50).reshape(n,50)
    return a[:,12:48].copy().view("<f4").reshape(n,3,3).astype(np.float64)

def look_at(eye,tgt,up):
    f=np.array(tgt,float)-np.array(eye,float); f/=np.linalg.norm(f)
    s=np.cross(f,np.array(up,float)); s/=np.linalg.norm(s)
    u=np.cross(s,f); return np.stack([s,u,f])

def render(items, path, size=(2200,1300), ss=2, eye_dir=(0.62,-0.62,0.48), up=(0,0,1)):
    W,H=size[0]*ss,size[1]*ss
    tris=[];cols=[];alpha=[]
    for p,c,a in items:
        tris.append(load(p)); cols.append(np.array(c,float)); alpha.append(a)
    allt=np.concatenate(tris); ctr=allt.reshape(-1,3).mean(0)
    d=np.array(eye_dir,float); d/=np.linalg.norm(d)
    eye=ctr+d*700.0; R=look_at(eye,ctr,up); pad=110*ss
    cam=[(t-eye)@R.T for t in tris]
    p2=[c[:,:,:2] for c in cam]; dep=[c[:,:,2] for c in cam]
    mn=np.concatenate([p.reshape(-1,2) for p in p2]).min(0)
    mx=np.concatenate([p.reshape(-1,2) for p in p2]).max(0)
    sc=min((W-2*pad)/max(1e-6,mx[0]-mn[0]),(H-2*pad)/max(1e-6,mx[1]-mn[1]))
    off=np.array([W/2,H/2])-(mn+mx)/2*sc
    pts=[p*sc+off for p in p2]
    for p in pts: p[:,:,1]=H-p[:,:,1]
    lights=np.array([[0.45,-0.45,-0.77],[-0.55,-0.25,-0.60],[0.05,0.65,-0.55],[0,0,-1]])
    lights/=np.linalg.norm(lights,axis=1,keepdims=True)
    img=np.empty((H,W,3),float); bg=np.array([236,235,231],float)
    img[...,0],img[...,1],img[...,2]=bg
    zbuf=np.full((H,W),1e9)
    def raster(ps,dp,t,c,a,blend):
        nrm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
        ln=np.linalg.norm(nrm,axis=1); ln[ln==0]=1; nrm/=ln[:,None]
        nv=nrm@R.T; vis=nv[:,2]<-0.02
        lam=(np.maximum(nv@lights.T,0)).sum(1)/len(lights)
        lam=np.clip(0.32+0.68*lam,0,1); rgb=np.clip(c*lam[:,None],0,1)*255
        for i in np.nonzero(vis)[0]:
            x,y,z=ps[i,:,0],ps[i,:,1],dp[i]
            x0,x1=int(max(0,np.floor(x.min()))),int(min(W-1,np.ceil(x.max())))
            y0,y1=int(max(0,np.floor(y.min()))),int(min(H-1,np.ceil(y.max())))
            if x1<=x0 or y1<=y0: continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1]
            d0=(y[1]-y[2])*(x[0]-x[2])+(x[2]-x[1])*(y[0]-y[2])
            if abs(d0)<1e-12: continue
            w0=((y[1]-y[2])*(xx-x[2])+(x[2]-x[1])*(yy-y[2]))/d0
            w1=((y[2]-y[0])*(xx-x[2])+(x[0]-x[2])*(yy-y[2]))/d0
            w2=1-w0-w1
            m=(w0>=-0.003)&(w1>=-0.003)&(w2>=-0.003)
            if not m.any(): continue
            zz=w0*z[0]+w1*z[1]+w2*z[2]
            upd=m&(zz<zbuf[y0:y1+1,x0:x1+1])
            if upd.any():
                if blend:
                    sub=img[y0:y1+1,x0:x1+1][upd]
                    zbuf[y0:y1+1,x0:x1+1][upd]=zz[upd]
                    img[y0:y1+1,x0:x1+1][upd]=a*rgb[i]+(1-a)*sub
                else:
                    zbuf[y0:y1+1,x0:x1+1][upd]=zz[upd]
                    img[y0:y1+1,x0:x1+1][upd]=rgb[i]
    for t,c,a,p,dp in zip(tris,cols,alpha,pts,dep):
        if a>=0.999: raster(p,dp,t,c,a,False)
    for t,c,a,p,dp in zip(tris,cols,alpha,pts,dep):
        if a<0.999: raster(p,dp,t,c,a,True)
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    im=im.resize(size, Image.LANCZOS)
    im.save(path)

P="/tmp/r_"
items=[
 ("parts/v1_back.stl",(0.66,0.71,0.79),1.0),
 ("parts/v1_cover.stl",(0.66,0.71,0.79),0.22),
 (P+"batt.stl",(0.85,0.76,0.62),1.0),
 (P+"pcb.stl",(0.20,0.44,0.31),1.0),
 (P+"shield.stl",(0.56,0.61,0.67),1.0),
 (P+"usbc.stl",(0.10,0.12,0.15),1.0),
 (P+"rtc.stl",(0.23,0.45,0.65),1.0),
 (P+"display.stl",(0.07,0.09,0.12),1.0),
 (P+"button.stl",(0.16,0.17,0.20),1.0),
 (P+"button_center.stl",(0.23,0.65,0.40),1.0),
 (P+"wire.stl",(0.85,0.62,0.18),1.0),
]
render(items, "FOB-1_3d_side.png", size=(2200,1300), ss=2, eye_dir=(0.55,-0.58,-0.60), up=(0,0,1))
print("FOB-1_3d_side.png")
