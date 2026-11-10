// simplify (keeping paint boundaries) and pack: header + uint16 pos + int8 nrm + uint8 rgba(a=material) + indices
const fs=require('fs');const _m=require('../dl_mo/mo/js/meshopt_simplifier.js'),S=_m.MeshoptSimplifier||_m;
const target=+process.argv[2]||90000,out=process.argv[3]||'sphinx.bin';
const f32=f=>new Float32Array(fs.readFileSync(f).buffer.slice(0));
(async()=>{await S.ready;S.useExperimentalFeatures=true;
 const P=f32('p.bin'),N=f32('n.bin'),C=f32('c.bin'),M=new Uint8Array(fs.readFileSync('m.bin')),F=new Uint32Array(fs.readFileSync('f.bin').buffer.slice(0));
 const nv=P.length/3;const A=new Float32Array(nv*6);for(let i=0;i<nv;i++){A[i*6]=C[i*4];A[i*6+1]=C[i*4+1]+M[i]*.5;A[i*6+2]=C[i*4+2];A[i*6+3]=N[i*3];A[i*6+4]=N[i*3+1];A[i*6+5]=N[i*3+2]}
 const [I,err]=S.simplifyWithAttributes(F,P,3,A,6,[1.2,1.2,1.2,.25,.25,.25],null,target*3,.004,[]);
 const [rem,un]=S.compactMesh(I);
 console.log('tris',F.length/3,'->',I.length/3,'verts',nv,'->',un,'err',err.toFixed(5));
 const mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9];const map=new Uint32Array(un);for(let i=0;i<nv;i++)if(rem[i]!==0xffffffff)map[rem[i]]=i;
 for(const i of map)for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],P[i*3+k]);mx[k]=Math.max(mx[k],P[i*3+k])}
 const big=un>65535,hdr=new ArrayBuffer(32),hv=new DataView(hdr);hv.setUint32(0,0x53504832,true);hv.setUint32(4,un,true);hv.setUint32(8,I.length,true);
 // pad header to 32: magic,nv,ni,(5 floats bbox would overflow) -> store bbox after
 const bb=new Float32Array([...mn,...mx]);
 const pos=new Uint16Array(un*3),nrm=new Int8Array(un*4),col=new Uint8Array(un*4);
 for(let j=0;j<un;j++){const i=map[j];for(let k=0;k<3;k++){pos[j*3+k]=Math.round((P[i*3+k]-mn[k])/(mx[k]-mn[k])*65535);nrm[j*4+k]=Math.round(N[i*3+k]*127);col[j*4+k]=Math.round(Math.min(1,C[i*4+k])*255)}nrm[j*4+3]=M[i];col[j*4+3]=Math.round(C[i*4+3]*255)}
 const idx=big?new Uint32Array(I):new Uint16Array(I);
 const parts=[new Uint8Array(hdr,0,12),new Uint8Array(bb.buffer),new Uint8Array(pos.buffer),new Uint8Array(pos.length%2?2:0),new Uint8Array(nrm.buffer),new Uint8Array(col.buffer),new Uint8Array(idx.buffer)];
 fs.writeFileSync(out,Buffer.concat(parts.map(p=>Buffer.from(p.buffer,p.byteOffset,p.byteLength))));
 console.log(out,fs.statSync(out).size,'bytes',big?'u32':'u16')})();
