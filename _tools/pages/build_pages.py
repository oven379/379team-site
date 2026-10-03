# -*- coding: utf-8 -*-
"""Сборка страниц услуг и портфолио itcompania.ru.

Запуск из корня репозитория:  python3 _tools/pages/build_pages.py
Данные: pages.py (страницы услуг), cases.py (проекты). Оформление берётся со страницы
/internet-magazin/, чтобы новые страницы выглядели как существующие.
"""
import os, re, sys, json, html, datetime
SCR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCR, '..', '..'))
sys.path.insert(0, SCR)
sys.path.insert(0, os.path.join(SCR, '..', 'blog'))
from pages import PAGES
from cases import APPS, SITES, PROJECTS
from metrika import add as add_metrika
from posts import POSTS as BLOG_A
from posts_plan import PLAN_POSTS as BLOG_B

SITE = 'https://itcompania.ru'
TG = 'https://t.me/manager379team'
ORG = {"@type": "Organization", "name": "It Компания", "url": SITE}

# --- какие статьи блога уже вышли (та же логика, что в генераторе блога: дата, 10:00 МСК)
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
TODAY = os.environ.get('BLOG_TODAY') or NOW.date().isoformat()
PUB_TODAY = bool(os.environ.get('BLOG_TODAY')) or NOW.hour >= 10
BLOG = {p['slug']: p for p in BLOG_A + BLOG_B}
def blog_live(slug):
    p = BLOG.get(slug)
    return bool(p) and (p['date'] < TODAY or (p['date'] == TODAY and PUB_TODAY))

# --- оформление с существующей страницы услуг
src = open(f'{ROOT}/internet-magazin/index.html', encoding='utf-8').read()
style = re.search(r'  <style>.*?</style>', src, re.S).group(0)
header = re.search(r'<header>.*?</header>', src, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', src, re.S).group(0)
fonts = re.search(r'  <link rel="preconnect".*?rel="stylesheet"/>', src, re.S).group(0)
script = re.search(r'<script>\s*function toggleFaq.*?</script>', src, re.S).group(0)

EXTRA = '''
    .cases-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
    .case{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:24px;display:flex;flex-direction:column;gap:10px}
    .case .kind{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--accent);font-weight:600}
    .case h3{font-size:19px;font-weight:700;color:var(--white)}
    .case p{color:var(--muted);font-size:14px;line-height:1.7;flex:1}
    .case-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:4px}
    .store-btn{display:inline-flex;align-items:center;gap:8px;background:#000;color:#fff;border:1px solid #444;border-radius:10px;padding:9px 14px;text-decoration:none;font-size:14px;font-weight:600;line-height:1.2}
    .store-btn:hover{border-color:var(--accent)}
    .store-btn small{display:block;font-size:10px;font-weight:400;opacity:.75}
    .text-link{color:var(--accent);font-size:14px;font-weight:600;text-decoration:none;align-self:center}
    .text-link:hover{text-decoration:underline}
    .sites-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
    .site-item{display:block;background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:16px 18px;text-decoration:none;transition:border-color .2s}
    .site-item:hover{border-color:var(--accent)}
    .site-item b{display:block;color:var(--white);font-size:15px;margin-bottom:4px}
    .site-item span{color:var(--muted);font-size:13px;line-height:1.5}
    .site-item i{display:block;font-style:normal;font-size:11px;color:var(--accent);margin-top:6px}
    .extra-link{display:inline-block;margin-top:20px;color:var(--accent);font-weight:600;text-decoration:none}
    .prose{max-width:820px}
    .prose h2{font-size:clamp(22px,3vw,30px);margin:40px 0 14px}
    .prose p,.prose li{color:#d6d6d6;font-size:16px;line-height:1.8}
    .prose p{margin-bottom:14px}
    .prose ul{margin:0 0 16px 22px}
    .prose li{margin-bottom:6px}
    .prose li::marker{color:var(--accent)}
    .prose a{color:var(--accent)}
    .prose strong{color:var(--white)}
    .prose .table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:10px;margin:8px 0 20px}
    .prose table{width:100%;border-collapse:collapse;font-size:15px}
    .prose th{background:var(--bg3);text-align:left;padding:12px 16px;color:var(--white)}
    .prose td{padding:12px 16px;border-top:1px solid var(--border);color:#d6d6d6;vertical-align:top}
    .terms-link{display:block;text-align:center;margin-top:18px;color:rgba(255,255,255,.6);font-size:14px}
    .terms-link:hover{color:var(--accent)}
    .page-intro{color:var(--muted);font-size:16px;line-height:1.75;max-width:720px;margin-bottom:32px}
    .process-wrap{max-width:1200px;margin:0 auto;padding:0 60px}
    .step h3,.include-item h3{overflow-wrap:break-word}
    @media(max-width:768px){.cases-grid,.sites-grid{grid-template-columns:1fr}.process-wrap{padding:0 20px}}
    @media(max-width:400px){.process-steps{grid-template-columns:1fr}}
  </style>'''
style_full = style.replace('\n  </style>', EXTRA)
APPLE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.37 12.62c.02 2.47 2.17 3.29 2.19 3.3-.02.06-.34 1.17-1.13 2.32-.68 1-1.39 1.99-2.5 2.01-1.1.02-1.45-.65-2.7-.65-1.26 0-1.65.63-2.69.67-1.07.04-1.89-1.08-2.58-2.07-1.4-2.03-2.48-5.73-1.04-8.23.72-1.24 1.99-2.03 3.37-2.05 1.05-.02 2.05.71 2.69.71.64 0 1.86-.88 3.13-.75.53.02 2.03.21 2.99 1.62-.08.05-1.78 1.04-1.76 3.11M14.3 5.3c.57-.69.96-1.65.85-2.61-.82.03-1.82.55-2.41 1.24-.53.61-.99 1.59-.87 2.53.92.07 1.85-.47 2.43-1.16"/></svg>'

def e(s): return html.escape(s, quote=True)

def head(title, desc, url, lds):
    ld = ''.join('\n  <script type="application/ld+json">\n  ' + json.dumps(x, ensure_ascii=False) + '\n  </script>' for x in lds)
    t = title.split(' | ')[0].split(' — ')[0]
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}"/>
  <meta name="robots" content="index, follow"/>
  <link rel="canonical" href="{url}"/>
  <meta property="og:type" content="website"/>
  <meta property="og:site_name" content="It Компания"/>
  <meta property="og:locale" content="ru_RU"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:title" content="{e(t)}"/>
  <meta property="og:description" content="{e(desc)}"/>
  <meta property="og:image" content="{SITE}/og-image.png"/>
  <meta property="og:image:width" content="1200"/>
  <meta property="og:image:height" content="630"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{e(t)}"/>
  <meta name="twitter:description" content="{e(desc)}"/>
  <meta name="twitter:image" content="{SITE}/og-image.png"/>
  <link rel="icon" type="image/x-icon" href="/favicon.ico"/>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>{ld}
{fonts}
{style_full}
  <style>[data-publish]:not(a){{display:none!important}}</style>
</head>
<body>
{header}
'''

TAIL = f'''
{footer}

{script}
<script src="/assets/publish.js" defer></script>
</body>
</html>
'''

def crumbs(*items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def app_card(a):
    links = [f'<a class="store-btn" href="{a["appstore"]}" target="_blank" rel="noopener">{APPLE}<span><small>Загрузите в</small>App Store</span></a>'] if a.get('appstore') else []
    if a.get('case'):
        links.append(f'<a class="text-link" href="{a["case"]}">Читать кейс →</a>')
    if a.get('site'):
        links.append(f'<a class="text-link" href="{a["site"]}" target="_blank" rel="noopener">Сайт проекта →</a>')
    return f'''
    <div class="case">
      <span class="kind">{a['kind']}</span>
      <h3>{a['name']}</h3>
      <p>{a['text']}</p>
      <div class="case-links">{''.join(links)}</div>
    </div>'''

def site_card(s):
    label = 'Behance' if s.get('behance') else s['url'].split('//')[1]
    return f'''
    <a class="site-item" href="{s['url']}" target="_blank" rel="noopener"><b>{s['name']}</b><span>{s['niche']}</span><i>{label} ↗</i></a>'''

def cases_for(tag):
    apps = [a for a in PROJECTS + APPS if a['confirmed'] and tag in a.get('tags', [])]
    sites = [s for s in SITES if tag in s.get('tags', []) or (tag == 'custom' and not s['tilda'])]
    if not apps and not sites:
        return ''
    body = ''
    if apps:
        body += '\n  <div class="cases-grid">' + ''.join(app_card(a) for a in apps) + '\n  </div>'
    if sites:
        body += '\n  <div class="sites-grid" style="margin-top:16px">' + ''.join(site_card(s) for s in sites) + '\n  </div>'
    return f'''
<section id="cases">
  <p class="section-label">Примеры работ</p>
  <h2>Наши проекты</h2>{body}
  <a class="extra-link" href="/portfolio/">Все работы →</a>
</section>
'''

def build_service(P):
    url = f"{SITE}/{P['slug']}/"
    num = re.sub(r'\D', '', P['price'])
    offer = {"@type": "Offer", "price": num, "priceCurrency": "RUB"} if num else None
    service = {"@context": "https://schema.org", "@type": "Service", "name": P['name'], "provider": ORG,
               "description": P['desc'], "url": url, "areaServed": "Russia"}
    if offer:
        service["offers"] = offer
    lds = [service, crumbs(("Главная", f"{SITE}/"), (P['name'], url)),
           {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
               {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P['faq']]}]
    inc = ''.join(f'\n    <div class="include-item">\n      <h3>{h}</h3>\n      <p>{t}</p>\n    </div>' for h, t in P['includes'])
    steps = ''.join(f'\n      <div class="step">\n        <div class="step-num">{i+1:02d}</div>\n        <h3>{h}</h3>\n        <p>{t}</p>\n      </div>' for i, (h, t) in enumerate(P['steps']))
    faq = ''.join(f'\n      <div class="faq-item">\n        <button class="faq-q" onclick="toggleFaq(this)">{q}<span class="arr">+</span></button>\n        <div class="faq-a">{a}</div>\n      </div>' for q, a in P['faq'])
    reads = [s for s in P.get('blog', []) if s in BLOG]
    read_html = ''
    if reads:
        items = ''.join(f'\n    <li data-publish="{BLOG[s]["date"]}"><a href="/blog/{s}/">{BLOG[s]["h1"]} →</a></li>' for s in reads)
        read_html = f'\n<section class="read-more" aria-label="Статьи по теме" data-list-box>\n  <p class="section-label">Полезно почитать</p>\n  <ul data-list="3">{items}\n  </ul>\n</section>\n'
    extra = f'\n  <a class="extra-link" href="{P["extra_link"][0]}">{P["extra_link"][1]}</a>' if P.get('extra_link') else ''
    h2, ctap = P['cta']
    page = head(P['title'], P['desc'], url, lds) + f'''
<div class="hero">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="/">Главная</a> → <span>{P['crumb']}</span>
  </nav>
  <p class="eyebrow">{P['eyebrow']}</p>
  <h1>{P['h1']}</h1>
  <p class="hero-sub">{P['sub']}</p>
  <div class="hero-actions">
    <a class="btn-primary" href="{TG}" target="_blank" rel="noopener">Получить бесплатную консультацию</a>
    <a class="btn-ghost" href="#includes">Что входит</a>
  </div>
  <div class="price-block">
    <div>
      <div class="price-num">{P['price']}</div>
      <div class="price-meta">{P['price_meta']}</div>
    </div>
    <div style="width:1px;height:60px;background:var(--border)"></div>
    <div>
      <div class="price-days">{P['days']}</div>
      <div class="price-meta">{P['days_meta']}</div>
    </div>
  </div>
</div>

<section id="includes">
  <p class="section-label">Состав работ</p>
  <h2>Что входит в работу</h2>
  <div class="includes-grid">{inc}
  </div>{extra}
</section>

<section style="background:var(--bg2);padding:80px 0">
  <div class="process-wrap">
    <p class="section-label">Процесс</p>
    <h2>{P.get('steps_title', 'Как мы работаем')}</h2>
    <div class="process-steps">{steps}
    </div>
  </div>
</section>
{cases_for(P['tags'][0])}
<section style="background:var(--bg2);padding:80px 0">
  <div class="process-wrap">
    <p class="section-label">Вопросы и ответы</p>
    <h2>Частые вопросы</h2>
    <div class="faq-list">{faq}
    </div>
  </div>
</section>
{read_html}
<div class="cta">
  <h2>{h2}</h2>
  <p>{ctap}</p>
  <a class="btn-primary" href="{TG}" target="_blank" rel="noopener">Написать в Telegram</a>
  <a class="terms-link" href="/usloviya-raboty/">Как мы работаем: договор, оплата, правки →</a>
</div>
''' + TAIL
    os.makedirs(f"{ROOT}/{P['slug']}", exist_ok=True)
    open(f"{ROOT}/{P['slug']}/index.html", 'w', encoding='utf-8').write(add_metrika(page))

def build_portfolio():
    url = f'{SITE}/portfolio/'
    apps = [a for a in APPS if a['confirmed']]
    lds = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Портфолио It Компании", "url": url,
            "description": "Мобильные приложения, CRM и сайты, которые мы разработали."},
           crumbs(("Главная", f"{SITE}/"), ("Портфолио", url))]
    page = head('Портфолио: сайты, мобильные приложения и CRM | It Компания',
                'Наши работы: мобильные приложения в App Store, CRM-система КарПас и сайты для бизнеса — от строительных компаний до ресторанов и автосервисов.',
                url, lds) + f'''
<div class="hero">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Главная</a> → <span>Портфолио</span></nav>
  <p class="eyebrow">Портфолио</p>
  <h1>Наши <em>работы</em></h1>
  <p class="hero-sub">Мобильные приложения, CRM и сайты, которые работают прямо сейчас. Приложения можно скачать, сайты — открыть и посмотреть.</p>
</div>

<section id="projects" style="padding-top:0">
  <p class="section-label">Кейсы</p>
  <h2>Проекты с разбором</h2>
  <div class="cases-grid">{''.join(app_card(a) for a in PROJECTS if a['confirmed'])}
  </div>
</section>

<section id="apps">
  <p class="section-label">Мобильные приложения и CRM</p>
  <h2>Приложения в App Store</h2>
  <p class="page-intro">Разрабатываем на React Native — одно приложение для iOS и Android. Подробнее — на странице <a href="/mobile/" style="color:var(--accent)">разработки мобильных приложений</a> и <a href="/razrabotka-crm-sistemy/" style="color:var(--accent)">разработки CRM</a>.</p>
  <div class="cases-grid">{''.join(app_card(a) for a in apps)}
  </div>
</section>

<section id="sites">
  <p class="section-label">Сайты</p>
  <h2>Сайты для бизнеса</h2>
  <p class="page-intro">Лендинги, многостраничные сайты и каталоги. Большинство сделано на Tilda — <a href="/blog/skolko-stoit-sajt-na-tilda/" style="color:var(--accent)">сколько это стоит</a>.</p>
  <div class="sites-grid">{''.join(site_card(s) for s in SITES)}
  </div>
</section>

<div class="cta">
  <h2>Обсудим ваш проект?</h2>
  <p>Расскажите о задаче в Telegram — покажем похожие работы и назовём стоимость.</p>
  <a class="btn-primary" href="{TG}" target="_blank" rel="noopener">Написать в Telegram</a>
</div>
''' + TAIL
    os.makedirs(f'{ROOT}/portfolio', exist_ok=True)
    open(f'{ROOT}/portfolio/index.html', 'w', encoding='utf-8').write(add_metrika(page))

def build_conditions():
    import conditions as C
    url = f'{SITE}/{C.SLUG}/'
    lds = [{"@context": "https://schema.org", "@type": "WebPage", "name": C.NAME, "url": url, "description": C.DESC},
           crumbs(("Главная", f"{SITE}/"), (C.NAME, url)),
           {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
               {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in C.FAQ]}]
    steps = ''.join(f'\n      <div class="step">\n        <div class="step-num">{i+1:02d}</div>\n        <h3>{h}</h3>\n        <p>{t}</p>\n      </div>' for i, (h, t) in enumerate(C.STEPS))
    faq = ''.join(f'\n      <div class="faq-item">\n        <button class="faq-q" onclick="toggleFaq(this)">{q}<span class="arr">+</span></button>\n        <div class="faq-a">{a}</div>\n      </div>' for q, a in C.FAQ)
    page = head(C.TITLE, C.DESC, url, lds) + f'''
<div class="hero">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Главная</a> → <span>{C.NAME}</span></nav>
  <p class="eyebrow">Условия работы</p>
  <h1>Как мы <em>работаем</em></h1>
  <p class="hero-sub">Обсуждение → бриф → договор → счёт и оплата → чек → разработка → сдача → поддержка. Все условия фиксируем заранее, а сайт, домен и доступы с первого дня оформлены на вас.</p>
</div>

<section style="background:var(--bg2);padding:80px 0">
  <div class="process-wrap">
    <p class="section-label">Этапы</p>
    <h2>От первого сообщения до запуска</h2>
    <div class="process-steps">{steps}
    </div>
  </div>
</section>

<section class="prose">{C.BODY}</section>

<section style="background:var(--bg2);padding:80px 0">
  <div class="process-wrap">
    <p class="section-label">Вопросы и ответы</p>
    <h2>Частые вопросы</h2>
    <div class="faq-list">{faq}
    </div>
  </div>
</section>

<div class="cta">
  <h2>Обсудим ваш проект?</h2>
  <p>Напишите в Telegram — ответим на вопросы и пришлём бриф.</p>
  <a class="btn-primary" href="{TG}" target="_blank" rel="noopener">Написать в Telegram</a>
</div>
''' + TAIL
    os.makedirs(f'{ROOT}/{C.SLUG}', exist_ok=True)
    open(f'{ROOT}/{C.SLUG}/index.html', 'w', encoding='utf-8').write(add_metrika(page))


for P in PAGES:
    build_service(P)
build_portfolio()
build_conditions()

# --- блок «Примеры работ» на существующих статичных страницах услуг (обновляется между метками)
INJECT = {'mobile': 'mobile', 'internet-magazin': 'shop'}
CSS_ONLY = EXTRA.replace('\n  </style>', '')
for slug, tag in INJECT.items():
    f = f'{ROOT}/{slug}/index.html'
    s = open(f, encoding='utf-8').read()
    block = cases_for(tag)
    s = re.sub(r'<!-- cases:start -->.*?<!-- cases:end -->\n\n', '', s, flags=re.S)
    s = re.sub(r'\n    /\* cases-css:start \*/.*?/\* cases-css:end \*/\n', '\n', s, flags=re.S)
    if block:
        anchor = '<section class="read-more"' if '<section class="read-more"' in s else '<div class="cta">'
        s = s.replace(anchor, '<!-- cases:start -->' + block + '<!-- cases:end -->\n\n' + anchor, 1)
        s = s.replace('\n  </style>', '\n    /* cases-css:start */' + CSS_ONLY + '\n    /* cases-css:end */\n  </style>', 1)
    open(f, 'w', encoding='utf-8').write(s)
print('блок работ добавлен на:', ', '.join(INJECT))

# --- карта сайта и llms.txt: блок страниц услуг и портфолио пересобирается целиком
slugs = [P['slug'] for P in PAGES] + ['portfolio', 'usloviya-raboty']
sm = open(f'{ROOT}/sitemap.xml', encoding='utf-8').read()
for s in slugs + ['sajt-onlajn-kursa']:  # старый адрес страницы онлайн-школы
    sm = re.sub(rf'  <url><loc>{SITE}/{s}/</loc>.*?</url>\n', '', sm)
PAGES_UPDATED = '2026-09-29'  # меняйте при правке текстов страниц услуг
rows = [f'  <url><loc>{SITE}/{s}/</loc><lastmod>{PAGES_UPDATED}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>' for s in slugs]
anchor = f'  <url><loc>{SITE}/blog/</loc>'
sm = sm.replace(anchor, '\n'.join(rows) + '\n' + anchor, 1) if anchor in sm else sm.replace('</urlset>', '\n'.join(rows) + '\n</urlset>')
open(f'{ROOT}/sitemap.xml', 'w', encoding='utf-8').write(sm)

ll = open(f'{ROOT}/llms.txt', encoding='utf-8').read()
ll = re.sub(r'- \[(Услуга|Портфолио|Условия работы)[^\n]*\n', '', ll)
lines = ''.join(f'- [Услуга — {P["name"]}]({SITE}/{P["slug"]}/)\n' for P in PAGES) + f'- [Портфолио: приложения, CRM и сайты]({SITE}/portfolio/)\n' + f'- [Условия работы: этапы, договор, оплата]({SITE}/usloviya-raboty/)\n'
ll = ll.replace('- [Блог](https://itcompania.ru/blog/)\n', lines + '- [Блог](https://itcompania.ru/blog/)\n', 1)
open(f'{ROOT}/llms.txt', 'w', encoding='utf-8').write(ll)
print('страницы:', ', '.join(slugs))

# Светлая тема и переключатель — на все страницы, включая только что собранные
import importlib.util as _u
_spec = _u.spec_from_file_location('apply_theme', os.path.join(ROOT, '_tools', 'theme', 'apply_theme.py'))
_m = _u.module_from_spec(_spec); _spec.loader.exec_module(_m); _m.main()
