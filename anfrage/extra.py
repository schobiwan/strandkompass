import urllib.request,urllib.parse,json,os
UA="StrandkompassBot/1.0 (https://github.com/schobiwan/strandkompass; info@nicoschober.com)"
os.makedirs("eingang/extra",exist_ok=True)
g=lambda u: urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=60).read()
u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",prop="imageinfo|revisions",rvprop="content",rvslots="main",titles="File:Mactra stultorum 02.jpg|File:Sandwich Tern (Thalasseus sandvicensis) (W1CDR0001504 BD9).ogg|File:Kittiwake (Rissa tridactyla) (W1CDR0001389 BD30).ogg",iiprop="url|extmetadata",iiurlwidth=3600,format="json",formatversion=2))
d=json.loads(g(u)); out={}
for p in d["query"]["pages"]:
    ii=p["imageinfo"][0]; out[p["title"]]={"wikitext":p["revisions"][0]["slots"]["main"]["content"][:2500],"thumb":ii.get("thumburl"),"meta":{k:v.get("value") for k,v in ii.get("extmetadata",{}).items() if k in("Artist","Credit","LicenseShortName","Attribution")}}
    if p["title"].endswith(".jpg"): open("eingang/extra/strahlenkoerbchen-gross.jpg","wb").write(g(ii["thumburl"]))
json.dump(out,open("eingang/extra/info.json","w"),ensure_ascii=False,indent=1)
