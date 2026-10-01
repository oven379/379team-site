import re, json, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrika import add as add_metrika
SCR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCR, '..', '..'))  # корень сайта: _tools/blog/../..
src = open(f'{ROOT}/internet-magazin/index.html').read()
style = re.search(r'  <style>.*?</style>', src, re.S).group(0)
header = re.search(r'<header>.*?</header>', src, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', src, re.S).group(0)
fonts = re.search(r'  <link rel="preconnect".*?rel="stylesheet"/>', src, re.S).group(0)

EXTRA = '''
    .article{max-width:780px;margin:0 auto;padding:0 60px 80px}
    .article-hero{max-width:780px;padding:64px 60px 32px}
    .article-hero h1{font-size:clamp(30px,4.2vw,50px);letter-spacing:-1px;line-height:1.1}
    .meta{color:var(--muted);font-size:14px}
    .article .lead{font-size:19px;color:var(--text);line-height:1.75;margin-bottom:8px}
    .article h2{font-size:clamp(24px,3vw,32px);margin:56px 0 16px}
    .article p{color:#d6d6d6;font-size:17px;line-height:1.8;margin-bottom:16px}
    .article a{color:var(--accent)}
    .article ul,.article ol{margin:0 0 20px 22px;color:#d6d6d6;font-size:17px;line-height:1.8}
    .article li{margin-bottom:8px}
    .article li::marker{color:var(--accent)}
    .article strong{color:var(--white)}
    .article .checklist{list-style:none;margin-left:0}
    .article .checklist li{padding-left:30px;position:relative}
    .article .checklist li::before{content:"✓";position:absolute;left:0;color:var(--accent);font-weight:700}
    .table-wrap{overflow-x:auto;margin:8px 0 24px;border:1px solid var(--border);border-radius:10px}
    .article table{width:100%;border-collapse:collapse;font-size:15px;min-width:520px}
    .article th{background:var(--bg3);text-align:left;padding:14px 16px;color:var(--white);font-weight:600}
    .article td{padding:14px 16px;border-top:1px solid var(--border);color:#d6d6d6;vertical-align:top;line-height:1.6}
    .flow{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:24px;margin:8px 0 24px}
    .flow-row{display:flex;align-items:stretch;gap:0;margin-bottom:14px}
    .node{flex:1;background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:12px;text-align:center;font-weight:600;font-size:14px;color:var(--white)}
    .node small{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:2px}
    .node.accent{border-color:var(--accent)}
    .arrow{flex:0 0 96px;display:flex;align-items:center;justify-content:center;position:relative}
    .arrow::before{content:"";position:absolute;left:6px;right:10px;top:50%;border-top:2px solid var(--accent)}
    .arrow::after{content:"";position:absolute;right:4px;top:calc(50% - 5px);border:5px solid transparent;border-left:8px solid var(--accent)}
    .arrow span{position:relative;top:-14px;font-size:11px;color:var(--muted);background:var(--bg2);padding:0 4px;text-align:center;line-height:1.2}
    .flow figcaption{color:var(--muted);font-size:13px;margin-top:4px}
    .faq-static dt{color:var(--white);font-weight:600;font-size:17px;margin-top:20px}
    .faq-static dd{color:#d6d6d6;font-size:16px;line-height:1.8;margin:6px 0 0}
    .related{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:48px}
    .related a{display:block;background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:20px;text-decoration:none;color:var(--text)}
    .related a:hover{border-color:var(--accent)}
    .related b{display:block;color:var(--white);margin-bottom:4px}
    .related span{color:var(--muted);font-size:14px}
    .posts{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
    .post-card{display:block;background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:28px;text-decoration:none;color:var(--text);transition:border-color .2s}
    .post-card:hover{border-color:var(--accent)}
    .post-card h2{font-size:22px;margin:8px 0 10px}
    .post-card p{color:var(--muted);font-size:15px;line-height:1.7}
    .post-card .more{color:var(--accent);font-weight:600;font-size:14px;margin-top:14px;display:inline-block}
    .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:24px 0 8px}
    .facts div{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
    .facts b{display:block;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--accent);margin-bottom:4px}
    .facts span{font-size:14px;color:var(--text)}
    .shot{margin:8px 0 24px}
    .shot img{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--border)}
    .shot figcaption{color:var(--muted);font-size:13px;margin-top:8px}
    .shots-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:560px}
    .article pre.template{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:18px 20px;margin:8px 0 24px;color:#d6d6d6;font-size:14px;line-height:1.7;white-space:pre-wrap;overflow-wrap:anywhere;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
    .article code{background:var(--bg3);border-radius:4px;padding:1px 6px;font-size:.9em}
    .more-posts{margin-top:48px}
    .more-posts h2{margin-top:0}
    .more-posts ul{list-style:none;margin:0}
    .more-posts li{border-top:1px solid var(--border);padding:14px 0;margin:0}
    .more-posts a{color:var(--text);text-decoration:none;font-weight:500}
    .more-posts a:hover{color:var(--accent)}
    h1{overflow-wrap:break-word}
    @media(max-width:380px){h1{font-size:30px;letter-spacing:-.5px}}
    @media(max-width:768px){
      .facts{grid-template-columns:1fr 1fr}
      .shots-2{gap:12px}
      .article{padding:0 20px 56px}
      .article-hero{padding:40px 20px 24px}
      .flow-row{flex-direction:column}
      .arrow{flex:0 0 40px}
      .arrow::before{left:50%;right:auto;top:4px;bottom:10px;border-top:0;border-left:2px solid var(--accent)}
      .arrow::after{right:auto;left:calc(50% - 4px);top:auto;bottom:2px;border:5px solid transparent;border-top:8px solid var(--accent)}
      .arrow span{top:auto;left:calc(50% + 14px);position:absolute;background:none;text-align:left}
      .related,.posts{grid-template-columns:1fr}
      .article table{min-width:0}
      .article thead{display:none}
      .article tr{display:block;border-top:1px solid var(--border);padding:12px 0}
      .article tbody tr:first-child{border-top:0}
      .article td{display:block;border:0;padding:4px 16px}
      .article td[data-label]:not([data-label=""])::before{content:attr(data-label);display:block;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--accent);margin-bottom:2px}
      .article td[data-label=""]{font-weight:600;color:var(--white);font-size:16px}
      .shot a::after{content:"Нажмите, чтобы увеличить";display:block;font-size:12px;color:var(--muted);margin-top:6px}
    }
  </style>'''
style_full = style.replace('\n  </style>', EXTRA)
header_blog = header.replace('<a href="/blog/" class="blog-link">', '<a href="/blog/" class="blog-link active" aria-current="page">', 1)

def e(s): return html.escape(s, quote=True)

def head(title, desc, url, ogtype, lds, image='https://itcompania.ru/og-image.png'):
    ld = ''.join('\n  <script type="application/ld+json">\n  ' + json.dumps(x, ensure_ascii=False) + '\n  </script>' for x in lds)
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}"/>
  <meta name="robots" content="index, follow, max-image-preview:large"/>
  <link rel="canonical" href="{url}"/>
  <meta property="og:type" content="{ogtype}"/>
  <meta property="og:site_name" content="It Компания"/>
  <meta property="og:locale" content="ru_RU"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:title" content="{e(title.split(' | ')[0])}"/>
  <meta property="og:description" content="{e(desc)}"/>
  <meta property="og:image" content="{image}"/>
  <meta property="og:image:width" content="1200"/>
  <meta property="og:image:height" content="630"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{e(title.split(' | ')[0])}"/>
  <meta name="twitter:description" content="{e(desc)}"/>
  <meta name="twitter:image" content="{image}"/>
  <link rel="icon" type="image/x-icon" href="/favicon.ico"/>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>{ld}
{fonts}
{style_full}
</head>
<body>
{header_blog}
'''

TAIL = f'''
{footer}
</body>
</html>
'''
ORG = {"@type": "Organization", "name": "It Компания", "url": "https://itcompania.ru", "logo": {"@type": "ImageObject", "url": "https://itcompania.ru/logo.png"}}
from posts import POSTS as ALL_POSTS, TG
from posts_plan import PLAN_POSTS
ALL_POSTS = ALL_POSTS + PLAN_POSTS
import datetime
# Публикация по таймеру без сервера: собираются ВСЕ статьи, а показывает их посетителям
# скрипт /assets/publish.js — в дату статьи в 10:00 по Москве (UTC+3).
# Карта сайта, llms.txt и JSON-LD блога содержат статьи, вышедшие на момент сборки,
# и обновляются при следующей выгрузке сайта на сервер.
PUBLISH_HOUR = 10
NOW_MSK = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
TODAY = NOW_MSK.date().isoformat()
def is_live(p):
    return p['date'] < TODAY or (p['date'] == TODAY and NOW_MSK.hour >= PUBLISH_HOUR)
ALL_SORTED = sorted(ALL_POSTS, key=lambda p: p['date'], reverse=True)
POSTS = [p for p in ALL_SORTED if is_live(p)]          # вышли на момент сборки
DATES = {p['slug']: p['date'] for p in ALL_POSTS}
SITE = 'https://itcompania.ru'
BURL = f'{SITE}/blog/'
PUBLISH_JS = '\n<script src="/assets/publish.js" defer></script>'
PUBLISH_CSS = ('\n  <style>[data-publish]:not(a){display:none!important}'
               '.gate-msg{display:none}.gated .gate-msg{display:block}'
               '.gated .article,.gated .article-hero .meta,.gated .cta{display:none}</style>')

def mobile_tables(html_):
    """Добавляет data-label к ячейкам: на телефоне строка таблицы показывается карточкой."""
    def fix(m):
        t = m.group(0)
        heads = re.findall(r'<th>(.*?)</th>', t)
        def row(r):
            i = iter(heads)
            return re.sub(r'<td>', lambda _: '<td data-label="%s">' % html.escape(re.sub('<[^>]+>', '', next(i, ''))), r.group(0))
        return re.sub(r'<tr>(?:(?!</tr>).)*<td>.*?</tr>', row, t, flags=re.S)
    return re.sub(r'<table>.*?</table>', fix, html_, flags=re.S)

def zoomable(html_):
    """Широкие скриншоты открываются в полном размере по нажатию."""
    return re.sub(r'(<figure class="shot">\s*)(<img src="([^"]+)" width="(\d+)"[^>]*/>)',
                  lambda m: m.group(1) + (f'<a href="{m.group(3)}" target="_blank" rel="noopener">{m.group(2)}</a>' if int(m.group(4)) > 1000 else m.group(2)), html_)

def mark_links(html_):
    """Ссылки на статьи блога помечаем датой выхода: до неё publish.js покажет их обычным текстом."""
    return re.sub(r'<a href="/blog/([a-z0-9-]+)/">',
                  lambda m: f'<a href="/blog/{m.group(1)}/" data-publish="{DATES[m.group(1)]}" data-inline>' if m.group(1) in DATES else m.group(0), html_)

def with_timer(page, gate=None):
    """Подключает таймер публикации к странице; gate — дата, до которой скрыт текст статьи."""
    page = page.replace('</head>', PUBLISH_CSS + '\n</head>', 1)
    if gate:
        page = page.replace('<html lang="ru">', f'<html lang="ru" data-gate="{gate}">', 1)
        page = page.replace('</head>', f"<script>if(new Date('{gate}T10:00:00+03:00')>new Date())document.documentElement.classList.add('gated')</script>\n</head>", 1)
    return page.replace('</body>', PUBLISH_JS + '\n</body>', 1)

def crumbs(*items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def build_post(A):
    url = f"{BURL}{A['slug']}/"
    img = SITE + A.get('image', '/og-image.png')
    lds = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": A['h1'], "description": A['desc'],
         "image": img, "datePublished": A['date'], "dateModified": A.get('modified', A['date']),
         "inLanguage": "ru", "author": ORG, "publisher": ORG,
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
        crumbs(("Главная", f"{SITE}/"), ("Блог", BURL), (A['crumb'], url)),
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in A['faq']]},
    ]
    body = mark_links(zoomable(mobile_tables(open(f"{SCR}/posts/{A['slug']}.html", encoding='utf-8').read())))
    faq_html = '<h2>Частые вопросы</h2>\n' if '<h2>Частые вопросы</h2>' not in body else ''
    faq_html += '<dl class="faq-static">\n' + ''.join(f'  <dt>{q}</dt>\n  <dd>{a}</dd>\n' for q, a in A['faq']) + '</dl>\n'
    related = ''.join(f'\n    <a href="{h}"><b>{t}</b><span>{s}</span></a>' for h, t, s in A['related'])
    # «Читайте также»: все остальные статьи, показываются 3 последних вышедших
    others = [p for p in ALL_SORTED if p['slug'] != A['slug']]
    more = ''.join(f'\n    <li data-publish="{p["date"]}"><a href="/blog/{p["slug"]}/">{p["h1"]}</a></li>' for p in others)
    h2, ctap = A['cta']
    page = head(A['title'], A['desc'], url, 'article', lds, img) + f'''
<div class="article-hero hero" style="margin:0 auto">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="/">Главная</a> → <a href="/blog/">Блог</a> → <span>{A['crumb']}</span>
  </nav>
  <p class="eyebrow">{A['eyebrow']}</p>
  <h1>{A['h1']}</h1>
  <p class="meta"><time datetime="{A['date']}">{A['date_h']}</time> · {A['read']} чтения · It Компания</p>
  <div class="gate-msg"><p class="hero-sub">Статья выйдет {A['date_h']} в 10:00 по Москве.</p><p class="meta" id="gate-msg"></p>
  <p style="margin-top:20px"><a class="btn-primary" href="/blog/">Все статьи блога</a></p></div>
</div>

<article class="article">
{body}{faq_html}
  <div class="related">{related}
  </div>
  <nav class="more-posts" aria-label="Читайте также" data-list-box>
    <h2>Читайте также</h2>
    <ul data-list="3">{more}
    </ul>
  </nav>
</article>

<div class="cta">
  <h2>{h2}</h2>
  <p>{ctap}</p>
  <a class="btn-primary" href="{TG}" target="_blank" rel="noopener">Написать в Telegram</a>
</div>
''' + TAIL
    os.makedirs(f"{ROOT}/blog/{A['slug']}", exist_ok=True)
    open(f"{ROOT}/blog/{A['slug']}/index.html", 'w', encoding='utf-8').write(add_metrika(with_timer(page, gate=A['date'])))

for A in ALL_SORTED:
    build_post(A)

blds = [
    {"@context": "https://schema.org", "@type": "Blog", "name": "Блог It Компании", "url": BURL, "publisher": ORG,
     "blogPost": [{"@type": "BlogPosting", "headline": p['h1'], "url": f"{BURL}{p['slug']}/", "datePublished": p['date']} for p in POSTS]},
    crumbs(("Главная", f"{SITE}/"), ("Блог", BURL)),
]
cards = ''.join(f'''
  <a class="post-card" href="/blog/{p['slug']}/" data-publish="{p['date']}">
    <span class="meta"><time datetime="{p['date']}">{p['date_h']}</time> · {p['read']}</span>
    <h2>{p['h1']}</h2>
    <p>{p['card']}</p>
    <span class="more">Читать →</span>
  </a>''' for p in ALL_SORTED)
bpage = head('Блог о разработке сайтов на Tilda, приложений и интеграций | It Компания',
             'Статьи и кейсы It Компании: сколько стоит сайт на Tilda, как выбрать формат сайта и разработчика, интеграции с Ozon и CRM, разработка мобильных приложений.',
             BURL, 'website', blds) + f'''
<div class="hero">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Главная</a> → <span>Блог</span></nav>
  <p class="eyebrow">Блог</p>
  <h1>Статьи и кейсы о сайтах на <em>Tilda</em> и digital-продуктах</h1>
  <p class="hero-sub">Рассказываем, сколько стоит сайт, как выбрать формат и подрядчика, и показываем наши проекты: интеграции, приложения, CRM.</p>
</div>
<section style="padding-top:0">
  <div class="posts" data-list="999">{cards}
  </div>
</section>
''' + TAIL
# карточки блога: CSS прячет [data-publish], но для a.post-card нужен явный селектор
bpage = with_timer(bpage).replace('[data-publish]:not(a){display:none!important}', '[data-publish]:not(a),a.post-card[data-publish]{display:none!important}', 1)
open(f'{ROOT}/blog/index.html', 'w', encoding='utf-8').write(add_metrika(bpage))
waiting = [p for p in ALL_SORTED if p not in POSTS]
print('вышли:', ', '.join(p['slug'] for p in POSTS))
if waiting: print('по таймеру:', ', '.join(f"{p['slug']} ({p['date']})" for p in reversed(waiting)))

# Карта сайта и llms.txt — статьи, вышедшие на момент сборки (обновятся при следующей выгрузке)
sm = open(f'{ROOT}/sitemap.xml', encoding='utf-8').read()
sm = re.sub(r'  <url><loc>https://itcompania.ru/blog/.*?</url>\n', '', sm)
rows = [f'  <url><loc>{BURL}</loc><lastmod>{POSTS[0]["date"] if POSTS else TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>']
rows += [f'  <url><loc>{BURL}{p["slug"]}/</loc><lastmod>{p.get("modified", p["date"])}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>' for p in POSTS]
open(f'{ROOT}/sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', '\n'.join(rows) + '\n</urlset>'))
ll = open(f'{ROOT}/llms.txt', encoding='utf-8').read()
ll = re.sub(r'- \[Статья: [^\n]*\n', '', ll)
ll = ll.replace('- [Блог](https://itcompania.ru/blog/)\n', '- [Блог](https://itcompania.ru/blog/)\n' + ''.join(f'- [Статья: {p["h1"]}]({BURL}{p["slug"]}/)\n' for p in POSTS), 1)
open(f'{ROOT}/llms.txt', 'w', encoding='utf-8').write(ll)

exec(open(f"{SCR}/page404.py", encoding="utf-8").read())
exec(open(f"{SCR}/admin.py", encoding="utf-8").read())

# Светлая тема и переключатель — на все страницы, включая только что собранные
import importlib.util as _u
_spec = _u.spec_from_file_location('apply_theme', os.path.join(ROOT, '_tools', 'theme', 'apply_theme.py'))
_m = _u.module_from_spec(_spec); _spec.loader.exec_module(_m); _m.main()
