# bake the restored paint scheme into vertex colours; material code per vertex (0 stone, 1 paint, 2 gold)
import numpy as np
f32=np.float32
z=np.load('sph_raw.npz');P,N,F,ao,own=z['P'],z['N'],z['F'],z['ao'],z['own']
n=len(P)
def h3(i,j,k):
    h=(i*73856093)^(j*19349663)^(k*83492791);h=(h^(h>>13))*1274126177;return ((h^(h>>16))&0xffff)/65535.0
def vnoise(Q,s):
    q=Q*s;i=np.floor(q).astype(np.int64);f=q-i;f=f*f*(3-2*f);r=0
    for dx in(0,1):
        for dy in(0,1):
            for dz in(0,1):
                w=(f[:,0] if dx else 1-f[:,0])*(f[:,1] if dy else 1-f[:,1])*(f[:,2] if dz else 1-f[:,2])
                r=r+w*h3(i[:,0]+dx,i[:,1]+dy,i[:,2]+dz)
    return r
def sm(a,b,x):t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
C=np.zeros((n,3),f32);M=np.zeros(n,np.uint8)
SAND=np.array([.74,.59,.41],f32);GOLD=np.array([1.0,.78,.34],f32);LAPIS=np.array([.07,.17,.52],f32)
TURQ=np.array([.16,.62,.60],f32);CARN=np.array([.72,.22,.12],f32);SKIN=np.array([.80,.47,.30],f32)
x,y,zz=P[:,0],P[:,1],P[:,2]
HO=np.array([0,.5,.3],f32);Q=P-HO;hx,hy,hz=Q[:,0],Q[:,1],Q[:,2]
# stone: strata, mottling, weathered crevices
n1=vnoise(P,1.1);n2=vnoise(P,4.0);n3=vnoise(P,11.0)
band=np.sin(y*5.6+n1*2.4)
stone=SAND[None]*(1+.055*band[:,None]+.12*(n1[:,None]-.5)+.07*(n2[:,None]-.5)+.05*(n3[:,None]-.5))
stone=stone*np.array([1,.99,.96],f32)+np.array([.02,0,-.02],f32)*(n2[:,None]-.5)
C[:]=stone
# painted detail is drawn per pixel in the shader; here: base tint (stone / skin / white), occlusion, and kind
K=own.astype(np.uint8)   # 0 stone 1 face 2 nemes 3 gold 4 beard
fsel=own==1;C[fsel]=np.array([.77,.55,.40],f32)*(1+.07*(n2[fsel,None]-.5))
psel=own>=2;C[psel]=(1+.05*(n3[psel,None]-.5))
C=np.clip(C,0,1);M=K
AO=np.clip(.3+.7*ao,0,1)
np.savez('sph_paint.npz',P=P,N=N,F=F,C=C,M=M)
P.astype(f32).tofile('p.bin');N.astype(f32).tofile('n.bin');np.concatenate([C,AO[:,None]],1).astype(f32).tofile('c.bin');M.astype(np.uint8).tofile('m.bin');F.astype(np.uint32).tofile('f.bin')
print(n,len(F),np.bincount(M))
