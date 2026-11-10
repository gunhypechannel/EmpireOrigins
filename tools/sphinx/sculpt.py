# Great Sphinx sculpt: signed-distance model -> marching cubes -> baked paint + ambient occlusion.
# Output raw arrays (sph_raw.npz) for simplification in node (meshoptimizer).
import numpy as np, sys
from skimage.measure import marching_cubes
f32=np.float32

def L(v):return np.sqrt(np.sum(v*v,axis=-1))
def smin(a,b,k):
    h=np.clip(.5+.5*(b-a)/k,0,1);return b*(1-h)+a*h-k*h*(1-h)
def smax(a,b,k):return -smin(-a,-b,k)
def ell(p,c,r):
    q=(p-np.array(c,f32))/np.array(r,f32);k0=L(q);k1=L(q/np.array(r,f32));return k0*(k0-1)/np.maximum(k1,1e-6)
def rcone(p,a,b,r1,r2):
    a=np.array(a,f32);b=np.array(b,f32);ba=b-a;l2=ba@ba;rr=r1-r2;a2=l2-rr*rr;il2=1/l2
    pa=p-a;y=pa@ba;z=y-l2;xv=pa*l2-y[...,None]*ba;x2=np.sum(xv*xv,-1);y2=y*y*l2;z2=z*z*l2
    k=np.sign(rr)*rr*rr*x2
    d=np.where(np.sign(z)*a2*z2>k,np.sqrt(x2+z2)*il2-r2,np.where(np.sign(y)*a2*y2<k,np.sqrt(x2+y2)*il2-r1,(np.sqrt(x2*a2*il2)+y*rr)*il2-r1))
    return d
def cap(p,a,b,r):return rcone(p,a,b,r,r)
def rot(ax,ang):
    c,s=np.cos(ang),np.sin(ang)
    if ax=='x':return np.array([[1,0,0],[0,c,-s],[0,s,c]],f32)
    if ax=='y':return np.array([[c,0,s],[0,1,0],[-s,0,c]],f32)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]],f32)
def rbox(p,c,h,r,R=None):
    q=p-np.array(c,f32)
    if R is not None:q=q@R            # world->local (R orthonormal, rows = local axes as columns)
    q=np.abs(q)-(np.array(h,f32)-r);return L(np.maximum(q,0))+np.minimum(np.max(q,-1),0)-r

# ---------------- the lion ----------------
def body(p):
    x=p[...,0]
    d=ell(p,(0,2.75,2.0),(1.72,1.75,1.5))
    d=smin(d,ell(p,(0,2.65,-.6),(1.78,1.78,2.9)),.9)
    d=smin(d,ell(p,(0,2.35,-3.3),(1.55,1.5,1.7)),.9)
    d=smin(d,ell(p,(0,2.45,-5.4),(1.78,1.8,1.95)),.8)
    d=smin(d,cap(p,(0,3.95,1.2),(0,4.0,-5.0),.35),.9)       # spine
    for s in(-1,1):
        d=smin(d,ell(p,(s*1.35,2.65,2.0),(.82,1.4,1.12)),.5)                       # shoulder
        d=smin(d,rcone(p,(s*1.38,2.2,2.5),(s*1.42,.78,3.6),.66,.56),.45)            # upper arm
        d=smin(d,rcone(p,(s*1.42,.74,3.6),(s*1.36,.6,6.55),.56,.46),.3)             # forearm
        d=smin(d,ell(p,(s*1.36,.5,6.95),(.72,.48,.86)),.3)                          # forepaw
        for i,t in enumerate((-.45,-.15,.15,.45)):
            d=smin(d,ell(p,(s*1.36+t,.36,7.62-abs(t)*.25),(.19,.2,.24)),.1)          # toes
        d=smin(d,ell(p,(s*1.45,2.05,-5.15),(.9,1.55,1.95)),.6)                      # haunch
        d=smin(d,rcone(p,(s*1.72,.75,-6.5),(s*1.88,.56,-3.6),.55,.42),.4)          # hock-to-foot
        d=smin(d,ell(p,(s*1.88,.45,-3.15),(.56,.42,.72)),.25)                       # hind paw
        for t in(-.3,0,.3):d=smin(d,ell(p,(s*1.88+t,.33,-2.55-abs(t)*.2),(.16,.17,.2)),.08)
    # tail curling round the right haunch
    pts=[(.9,1.2,-7.25),(1.8,.55,-7.05),(2.42,.42,-5.9),(2.5,.42,-4.6),(2.42,.45,-3.7)]
    for a,b in zip(pts,pts[1:]):d=smin(d,cap(p,a,b,.2),.12)
    d=smin(d,ell(p,(2.34,.48,-3.35),(.27,.24,.36)),.1)
    d=smin(d,rcone(p,(0,3.9,2.3),(0,5.75,3.3),.98,.7),.45)                          # neck
    return np.maximum(d,.12-p[...,1])                                                # lies flat on its base
def faceS(p):
    d=ell(p,(0,6.0,3.05),(.86,.94,.88))
    d=smin(d,ell(p,(0,5.83,3.45),(.57,.82,.56)),.25)
    d=smin(d,ell(p,(0,5.18,3.58),(.38,.36,.4)),.16)
    d=smin(d,ell(p,(0,6.25,3.84),(.5,.08,.13)),.1)                                   # brow
    d=smin(d,rcone(p,(0,6.05,3.98),(0,5.66,4.17),.06,.1),.07)                        # nose
    d=smin(d,ell(p,(0,5.67,4.1),(.14,.06,.07)),.04)                                  # nostril wings
    d=smin(d,ell(p,(0,5.47,3.95),(.2,.05,.07)),.04);d=smin(d,ell(p,(0,5.4,3.93),(.17,.045,.07)),.04);d=smax(d,-ell(p,(0,5.435,4.03),(.17,.008,.05)),.01)   # lips + parting
    for s in(-1,1):
        d=smin(d,ell(p,(s*.31,5.74,3.72),(.2,.24,.19)),.12)                         # cheeks
        d=smax(d,-ell(p,(s*.25,6.03,4.03),(.16,.1,.09)),.05)                          # eye socket
        d=smin(d,ell(p,(s*.25,6.0,3.93),(.125,.058,.075)),.03)                      # eyeball
    return d
def nemesS(p):
    d=ell(p,(0,6.2,2.95),(1.0,1.02,1.08))
    d=smin(d,rcone(p,(0,6.0,2.0),(0,4.7,1.65),.6,.38),.3)                           # queue down the back
    for s in(-1,1):
        d=smin(d,rbox(p,(s*1.08,5.3,3.0),(.17,.98,.56),.08,rot('z',s*.26)),.25)       # flaring side panels
        d=smin(d,rbox(p,(s*.86,4.42,3.6),(.27,.9,.09),.06,rot('x',-.12)),.12)        # lappets on the chest
    d=smax(d,-rbox(p,(0,5.72,4.0),(.66,.76,.75),.18),.08)                            # open for the face
    return d
def goldS(p):
    d=rbox(p,(0,6.44,3.88),(.66,.065,.1),.04,rot('x',.15))                           # brow band
    d=np.minimum(d,cap(p,(0,6.44,3.98),(0,6.86,4.02),.07))                          # uraeus
    d=smin(d,ell(p,(0,6.88,4.04),(.13,.17,.055)),.04)
    return d
def beardS(p):
    d=rcone(p,(0,5.16,3.74),(0,4.48,3.86),.14,.12)
    return smin(d,ell(p,(0,4.42,3.93),(.15,.12,.12)),.05)
HO=np.array([0,.5,.3],f32)
def parts(p):q=p-HO;return [body(p),faceS(q),nemesS(q),goldS(q),beardS(q)]
def sdf(p):
    b,fa,n,g,br=parts(p);d=smin(b,fa,.25);return np.minimum(np.minimum(d,n),np.minimum(g,br))

# ---------------- mesh ----------------
VX=float(sys.argv[1]) if len(sys.argv)>1 else .045
lo=np.array([-2.95,0.0,-7.9],f32);hi=np.array([2.95,7.95,8.0],f32)
nx,ny,nz=[int(np.ceil((hi[i]-lo[i])/VX))+1 for i in range(3)]
print('grid',nx,ny,nz,flush=True)
xs=lo[0]+np.arange(nx,dtype=f32)*VX;ys=lo[1]+np.arange(ny,dtype=f32)*VX;zs=lo[2]+np.arange(nz,dtype=f32)*VX
V=np.empty((nx,ny,nz),f32)
X,Y=np.meshgrid(xs,ys,indexing='ij')
for k in range(nz):
    P=np.stack([X,Y,np.full_like(X,zs[k])],-1);V[:,:,k]=sdf(P)
    if k%60==0:print('z',k,flush=True)
V[:,0,:]=np.maximum(V[:,0,:],.001)      # close the bottom
verts,faces,_,_=marching_cubes(V,0,spacing=(VX,VX,VX))
verts=verts+lo;faces=faces.copy()
print('mc',len(verts),len(faces),flush=True)

# normals from the field gradient
e=.01
def grad(P):
    g=np.stack([sdf(P+np.array([e,0,0],f32))-sdf(P-np.array([e,0,0],f32)),sdf(P+np.array([0,e,0],f32))-sdf(P-np.array([0,e,0],f32)),sdf(P+np.array([0,0,e],f32))-sdf(P-np.array([0,0,e],f32))],-1)
    return g/np.maximum(L(g)[...,None],1e-6)
P=verts.astype(f32);N=grad(P)
# ambient occlusion along the normal + a ground term
ao=np.zeros(len(P),f32)
for i,h in enumerate((.08,.18,.35,.6,1.0)):
    ao+=(h-np.maximum(sdf(P+N*h),0)*1.0)/h*(.5**i)
ao=np.clip(1-ao*.55,0,1)
# hemisphere-ish: down-facing and creased spots darker
ao*=np.clip(.72+.28*(N[:,1]*.5+.5),0,1)
ao*=np.clip(.62+P[:,1]*.16,0,1)**.6
# which part owns each vertex
D=np.stack(parts(P),-1);own=np.argmin(D,-1)
np.savez('sph_raw.npz',P=P,N=N,F=faces.astype(np.uint32),ao=ao,own=own)
print('saved',len(P))
