import json,re,sys
ns={};exec(open('hyp_lines.py').read(),ns);R=ns['R']
V=json.load(open('vlines5.json'))
def build(hero):
    h={};exec(open(f'heroes/{hero}.py').read(),h);L=h['L']
    assert len(L)==len(R),(hero,len(L),len(R))
    for i,((p,_),t) in enumerate(zip(R,L)):
        if ('(?P<n>' in p)!=('{n}' in t): print('N MISMATCH',i,t)
    m={}
    for old in V[hero]:
        for (p,_),t in zip(R,L):
            mm=re.fullmatch(p.replace("I'm Hypatia","I'm \\w+"),old)
            if mm: m[old]=t.replace('{n}',mm.group('n')) if '{n}' in t else t;break
        else: print('NO RULE',hero,old)
    return m
if __name__=='__main__':
    hero=sys.argv[1];m=build(hero)
    u=set(m.values());c=[x for x in u if re.search(r'\bchief\b',x,re.I)]
    print(hero,'lines',len(m),'unique',len(u),'chars',sum(len(x) for x in u),'chief',len(c),c)
    json.dump(m,open(f'heroes/{hero}_map.json','w'),indent=0,ensure_ascii=False)
