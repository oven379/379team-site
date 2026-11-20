# -*- coding: utf-8 -*-
"""Read-only technical SEO audit. Run: python3 _tools/audit_site.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import defaultdict
import datetime, json, re, sys, xml.etree.ElementTree as ET
from urllib.robotparser import RobotFileParser
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://itcompania.ru'
sys.path.insert(0,str(ROOT/'_tools/blog'))
from posts import POSTS
from posts_plan import PLAN_POSTS
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
FUTURE = {SITE+'/blog/'+p['slug']+'/':p for p in POSTS+PLAN_POSTS if datetime.datetime.fromisoformat(p['date']+'T10:00:00+03:00')>NOW}
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.title='';self.h1=0;self.ids=[];self.meta={};self.canon=[];self.links=[];self.images=[];self.structured=[];self.in_title=False;self.in_ld=False
    def handle_starttag(self,t,a):
        d=dict(a)
        if t=='title':self.in_title=True
        if t=='script':self.in_ld=d.get('type')=='application/ld+json'
        if t=='h1':self.h1+=1
        if d.get('id'):self.ids.append(d['id'])
        if t=='meta':self.meta[d.get('name',d.get('property',''))]=d.get('content','')
        if t=='link' and d.get('rel')=='canonical':self.canon.append(d.get('href',''))
        if t=='img':self.images.append(d)
        for k in ['href','src']:
            if k in d:self.links.append(d[k])
    def handle_data(self,s):
        if self.in_title:self.title+=s
        if self.in_ld and s.strip():self.structured.append(json.loads(s))
    def handle_endtag(self,t):
        if t=='title':self.in_title=False
        if t=='script':self.in_ld=False

def pages():
    return sorted([ROOT/'index.html',ROOT/'404.html',*ROOT.glob('*/index.html'),*ROOT.glob('blog/*/index.html')])
def url_of(p):
    return SITE+'/'+str(p.relative_to(ROOT)).replace('index.html','')
def main():
    parsed={};errors=[];warnings=[];titles=defaultdict(list);descs=defaultdict(list)
    for p in pages():
        a=Page()
        try:a.feed(p.read_text())
        except Exception as e:errors.append((str(p.relative_to(ROOT)),'HTML/JSON-LD: '+str(e)));continue
        parsed[p.resolve()]=a
    for p,a in parsed.items():
        path=str(p.relative_to(ROOT));url=url_of(p);noindex='noindex' in a.meta.get('robots','')
        def err(msg):errors.append((path,msg))
        if not noindex:
            if a.h1!=1:err(f'H1 count: {a.h1}')
            if a.canon!=[url]:err(f'canonical mismatch: {a.canon}')
            if a.meta.get('og:url')!=url:err('og:url mismatch')
            if not a.structured:err('missing JSON-LD')
            titles[a.title].append(path);descs[a.meta.get('description','')].append(path)
        if not a.title:err('missing title')
        if not a.meta.get('description'):err('missing description')
        if len(a.ids)!=len(set(a.ids)):err('duplicate IDs')
        if a.meta.get('viewport') is None:err('missing viewport')
        for img in a.images:
            if 'alt' not in img:err('missing image alt: '+img.get('src',''))
            if 'width' not in img or 'height' not in img:warnings.append((path,'image without intrinsic dimensions: '+img.get('src','')))
        for ref in a.links:
            u=urlsplit(ref)
            if u.netloc and u.netloc!='itcompania.ru':continue
            if u.scheme and u.scheme not in ['http','https']:continue
            if u.netloc=='itcompania.ru' and u.scheme!='https':err('non-HTTPS internal link: '+ref)
            if not u.path:target=p
            elif u.path.startswith('/'):target=ROOT/unquote(u.path.lstrip('/'))
            else:target=p.parent/unquote(u.path)
            if target.is_dir():target=target/'index.html'
            if not target.exists():err('missing local resource: '+ref);continue
            if u.fragment and target.resolve() in parsed and unquote(u.fragment) not in parsed[target.resolve()].ids:err('missing anchor: '+ref)
    for name,group in [('title',titles),('description',descs)]:
        for val,paths in group.items():
            if val and len(paths)>1:errors.append((', '.join(paths),'duplicate '+name))
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sm=ET.parse(ROOT/'sitemap.xml');urls=[x.text for x in sm.findall('.//s:loc',ns)]
    if len(urls)!=len(set(urls)):errors.append(('sitemap.xml','duplicate URLs'))
    expected={url_of(p) for p,a in parsed.items() if 'noindex' not in a.meta.get('robots','') and url_of(p) not in FUTURE}
    for url in sorted(expected-set(urls)):errors.append(('sitemap.xml','missing published page: '+url))
    for url in sorted(set(urls)-expected):errors.append(('sitemap.xml','non-public/unknown URL: '+url))
    for entry in sm.findall('.//s:url',ns):
        date=entry.find('s:lastmod',ns)
        if date is not None and date.text>NOW.date().isoformat():errors.append(('sitemap.xml','future lastmod '+date.text))
    feed=ET.parse(ROOT/'feed.yml');offers=feed.findall('.//offer')
    for offer in offers:
        price=offer.findtext('price');url=offer.findtext('url');p=ROOT/(urlsplit(url).path.lstrip('/'))/'index.html'
        a=parsed.get(p.resolve())
        if not a:errors.append(('feed.yml','unknown service '+str(url)))
        if a and price not in re.sub(r'[\s\u00a0\u202f]','',p.read_text()):errors.append(('feed.yml','price absent on service '+str(url)))
    robots=RobotFileParser();robots.parse((ROOT/'robots.txt').read_text().splitlines())
    for bot in ['Googlebot','Yandex','GPTBot']:
        for path in ['/admin/','/_tools/','/.git/HEAD']:
            if robots.can_fetch(bot,SITE+path):errors.append(('robots.txt',bot+' allowed '+path))
        if not robots.can_fetch(bot,SITE+'/lending/'):errors.append(('robots.txt',bot+' blocked public service'))
    print(json.dumps({'pages':len(parsed),'sitemap_urls':len(urls),'feed_offers':len(offers),'scheduled_posts':len(FUTURE),'errors':errors,'warnings':warnings},ensure_ascii=False,indent=2))
    return bool(errors)
if __name__=='__main__':sys.exit(main())
