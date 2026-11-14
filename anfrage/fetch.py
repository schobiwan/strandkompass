import json,urllib.request,urllib.parse,re,html,sys,os,time
UA="StrandkompassBot/1.0 (https://github.com/schobiwan/strandkompass; info@nicoschober.com)"
def get(u,b=False):
    for i in range(5):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=40).read()
            return r if b else json.loads(r)
        except Exception as e:
            print("retry",e,file=sys.stderr); time.sleep(20*(i+1))
def api(**p): return get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(p,format="json",formatversion=2,maxlag=5)))
strip=lambda s: html.unescape(re.sub(r"<[^>]+>","",s or "")).strip()
L=json.load(open(sys.argv[1])); out=sys.argv[2]
meta=json.load(open(out+"/meta.json")) if os.path.exists(out+"/meta.json") else {}
for k,q in L.items():
    if meta.get(k): continue
    d=api(action="query",generator="search",gsrsearch=q+" filetype:bitmap",gsrnamespace=6,gsrlimit=5,prop="imageinfo",iiprop="url|extmetadata|size",iiurlwidth=960)
    pages=sorted(d.get("query",{}).get("pages",[]),key=lambda p:p.get("index",0)) if d else []
    meta[k]=[]
    for i,p in enumerate(pages):
        if "imageinfo" not in p: continue
        ii=p["imageinfo"][0]; md=ii.get("extmetadata",{})
        lic=strip(md.get("LicenseShortName",{}).get("value"))
        if not re.search(r"CC BY|CC0|Public domain",lic,re.I) or "NC" in lic or "ND" in lic: continue
        time.sleep(1.5)
        data=get(ii.get("thumburl") or ii["url"],True)
        if not data: continue
        fn=f"{k}-{i}.jpg"; open(f"{out}/{fn}","wb").write(data)
        meta[k].append(dict(file=fn,title=p["title"],url=ii["descriptionurl"],artist=strip(md.get("Artist",{}).get("value"))[:80],license=lic,w=ii["width"],h=ii["height"]))
    print(k,len(meta[k]),flush=True)
    json.dump(meta,open(out+"/meta.json","w"),ensure_ascii=False,indent=1)
    time.sleep(3)
