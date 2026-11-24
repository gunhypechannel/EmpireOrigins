import json,subprocess,re,math,sys,statistics as st
S='hypv/'
G=json.load(open('hyp_groups.json'))['groups']
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
groups=[int(x) for x in sys.argv[1:]] or range(len(G))
for g in groups:
    L=G[g];f=S+f'raw/G{g}.wav';d=dur(f);P=sil(f)
    lead=P[0][1] if P and P[0][0]<0.05 else 0.0
    tail=P[-1][0] if P and P[-1][1]>d-0.05 else d
    C=[p for p in P if p[0]>lead+0.05 and p[1]<tail-0.05]
    n=len(L);w=[len(t)+12 for t in L];W=sum(w)
    speech=(tail-lead)-sum(p[1]-p[0] for p in C)*0  # approx
    # positions: boundary k between line k and k+1 chosen from C (index), monotone
    pts=[lead]+[None]*(n-1)+[tail]
    m=len(C);INF=1e18
    # dp[k][j]: best cost with boundary k at gap j
    exp=[(tail-lead)*wi/W for wi in w]
    def segcost(a,b,i):
        x=(b-a)/exp[i];return (math.log(max(x,1e-3)))**2
    dp=[[INF]*m for _ in range(n)];bk=[[-1]*m for _ in range(n)]
    for j in range(m):
        dp[1][j]=segcost(lead,C[j][0],0)-1.5*(C[j][1]-C[j][0])
    for k in range(2,n):
        for j in range(m):
            gj=C[j];best=INF;bi=-1
            for i in range(j):
                if dp[k-1][i]>=INF:continue
                c=dp[k-1][i]+segcost(C[i][1],gj[0],k-1)
                if c<best:best=c;bi=i
            if bi>=0:dp[k][j]=best-1.5*(gj[1]-gj[0]);bk[k][j]=bi
    best=INF;bj=-1
    for j in range(m):
        if dp[n-1][j]<INF:
            c=dp[n-1][j]+segcost(C[j][1],tail,n-1)
            if c<best:best=c;bj=j
    sel=[];j=bj;k=n-1
    while k>=1:sel.append(j);j=bk[k][j];k-=1
    sel=sel[::-1];gaps=[C[j] for j in sel]
    b=[lead]+[x for p in gaps for x in (p[0],p[1])]+[tail]
    R=[]
    for i,txt in enumerate(L):
        a=max(0,b[2*i]-.06);e=min(d,b[2*i+1]+.12);o=S+f'clips/{key(txt)}.mp3';cut(f,a,e,o);R.append(((b[2*i+1]-b[2*i])/exp[i],txt))
    bad=[(round(r,2),t[:40]) for r,t in R if r>1.5 or r<0.6]
    print(g,'cost',round(best,2),'bad',bad)
