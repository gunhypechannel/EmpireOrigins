import subprocess,re,os,json
S='/tmp/claude-0/-home-claude/029486ea-9d8e-56c6-bf0e-860adae5556b/scratchpad/'
D=[(l.split()[0],float(l.split()[1])) for l in open(S+'hyp_durs.txt')]
H=json.load(open(S+'hyp_groups.json'));G=H['groups'];F6=H['first6']
os.makedirs(S+'hypv/raw',exist_ok=True);os.makedirs(S+'hypv/clips',exist_ok=True)
t=0
for name,d in D:
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.4f}','-t',f'{d:.4f}','-i',S+'hypv/all.mp3','-c:a','pcm_s16le','-ac','1','-ar','44100',S+f'hypv/raw/{name}.wav']);t+=d
def sil(f):
    e=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=noise=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
    return list(zip([float(x) for x in re.findall(r'silence_start: (-?[0-9.]+)',e)],[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',e)]))
def dur(f):return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def key(x):
    n=re.sub(r'[^a-z0-9]+','',x.lower());h=0x811c9dc5
    for ch in n.encode():h=((h^ch)*0x01000193)&0xffffffff
    return format(h,'08x')
def cut(f,a,b,o):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.3f}','-to',f'{b:.3f}','-i',f,'-af','afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,loudnorm=I=-17:TP=-1.5:LRA=11','-ac','1','-ar','24000','-c:a','libmp3lame','-b:a','40k',o])
rep={};out={}
def bounds(f):
    d=dur(f);P=sil(f)
    lead=P[0][1] if P and P[0][0]<0.05 else 0.0
    tail=P[-1][0] if P and P[-1][1]>d-0.05 else d
    return d,P,lead,tail
for i,txt in enumerate(F6):
    f=S+f'hypv/raw/S{i}.wav';d,P,lead,tail=bounds(f);o=S+f'hypv/clips/{key(txt)}.mp3';cut(f,max(0,lead-.06),min(d,tail+.12),o);out[key(txt)]=txt
for g,L in enumerate(G):
    f=S+f'hypv/raw/G{g}.wav';d,P,lead,tail=bounds(f);n=len(L)
    inner=[p for p in P if p[0]>lead+0.05 and p[1]<tail-0.05]
    byg=sorted(inner,key=lambda p:p[1]-p[0],reverse=True)
    gaps=sorted(byg[:n-1]);gl=[round(p[1]-p[0],2) for p in byg[:n+1]]
    ok=len(byg)>=n-1 and (len(byg)<n or gl[n-2]>gl[n-1]*1.4 if len(gl)>=n else True)
    rep[g]=(n,len(inner),gl[max(0,n-3):n+1],ok)
    b=[lead]+[x for p in gaps for x in (p[0],p[1])]+[tail]
    for i,txt in enumerate(L):
        a=max(0,b[2*i]-.06);e=min(d,b[2*i+1]+.12);o=S+f'hypv/clips/{key(txt)}.mp3';cut(f,a,e,o);out[key(txt)]=txt
json.dump(out,open(S+'hypv/clips_map.json','w'),ensure_ascii=False)
for k,v in rep.items():print(k,v)
print(len(out))
