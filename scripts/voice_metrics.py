import re,sys,json
def sections(text):
    parts=re.split(r'(?m)^(## .+)$',text)
    out=[]
    for i in range(1,len(parts),2):
        out.append((parts[i][3:].strip(),parts[i+1]))
    return out
def prose(body):
    lines=[]
    for l in body.splitlines():
        s=l.strip()
        if not s or s.startswith('#') or s.startswith('|') or s.startswith('![') or s.startswith('**Gate') or s.startswith('**Figure'): continue
        lines.append(s)
    t='\n'.join(lines)
    t=re.sub(r'\]\([^)]+\)',']',t); t=t.replace('**','').replace('_Field note:','Field note:')
    return t
def sents(t):
    t=re.sub(r'\b(e\.g|i\.e|vs|Dr|Mr|No)\.', lambda m:m.group(1),t)
    ss=re.split(r'(?<=[.!?])["”’)]*\s+|\n',t)
    return [s for s in ss if re.search(r'[A-Za-z]',s)]
def m(body):
    t=prose(body); w=re.findall(r"[A-Za-z0-9’'%$-]+",t); ss=sents(t)
    sw=[len(re.findall(r"[A-Za-z0-9’'%$-]+",s)) for s in ss]
    low=t.lower()
    return dict(words=len(w),sent=len(ss),short=round(100*sum(1 for x in sw if x<=6)/max(1,len(ss))),
      we=len(re.findall(r"\b(we|we're|we’re|we've|we’ve|our|us)\b",low)),
      asides=len(re.findall(r"\([^)]{1,120}\)",t)),
      evidence=len(re.findall(r"\bevidence",low)),establish=len(re.findall(r"\bestablish",low)),
      neg=len(re.findall(r"\b(does not|do not|cannot|did not|is not)\b",low)),
      contr=len(re.findall(r"\b\w+(n’t|n't|’s|'s|’re|'re|’ve|'ve|’ll|'ll|’m|'m|’d|'d)\b",low)))
if __name__=='__main__':
    text=open(sys.argv[1]).read()
    for title,body in sections(text):
        r=m(body)
        print(f"{title[:42]:42} w{r['words']:5} short{r['short']:3}% we{r['we']:3} as{r['asides']:3} ev{r['evidence']:3} est{r['establish']:3} neg{r['neg']:3} con{r['contr']:3}")
