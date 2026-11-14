import json,urllib.request,urllib.parse,re,html,sys,os,time
UA="StrandkompassBot/1.0 (https://github.com/schobiwan/strandkompass; info@nicoschober.com)"
def get(u,b=False):
    for i in range(4):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=60).read()
            return r if b else json.loads(r)
        except Exception as e: print("retry",e); time.sleep(5*(i+1))
strip=lambda s: html.unescape(re.sub(r"<[^>]+>","",s or "")).strip()
L=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True); meta={}
for k,q in L.items():
    d=get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",generator="search",gsrsearch=f'"{q}" filetype:audio',gsrnamespace=6,gsrlimit=8,prop="imageinfo",iiprop="url|extmetadata|size",format="json",formatversion=2)))
    pages=sorted((d or {}).get("query",{}).get("pages",[]),key=lambda p:p.get("index",0)); meta[k]=[]
    for i,p in enumerate(pages):
        ii=p.get("imageinfo",[{}])[0]; md=ii.get("extmetadata",{}); lic=strip(md.get("LicenseShortName",{}).get("value"))
        if not re.search(r"CC BY|CC0|Public domain",lic,re.I) or "NC" in lic or "ND" in lic or (ii.get("size") or 0)>20_000_000: continue
        if len(meta[k])>=3: break
        ext=ii["url"].rsplit(".",1)[1].lower(); data=get(ii["url"],True)
        if not data: continue
        fn=f"{k}-{i}.{ext}"; open(f"{out}/{fn}","wb").write(data)
        meta[k].append(dict(file=fn,title=p["title"],url=ii["descriptionurl"],artist=strip(md.get("Artist",{}).get("value"))[:80],license=lic,duration=ii.get("duration")))
        time.sleep(1)
    print(k,len(meta[k]))
json.dump(meta,open(out+"/meta.json","w"),ensure_ascii=False,indent=1)
