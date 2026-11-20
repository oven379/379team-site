# -*- coding: utf-8 -*-
"""Общее оформление и навигация. Запускать после сборки страниц и блога."""
import glob, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
THEME_VER = '9'
INLINE = ("<script>try{if(localStorage.getItem('itc-theme')==='dark')"
          "document.documentElement.removeAttribute('data-theme');"
          "else document.documentElement.setAttribute('data-theme','light');"
          "if(localStorage.getItem('itc-cookies')==='no')window['disableYaCounter113101565']=true"
          "}catch(e){}</script>")
SUN = '<svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/></svg>'
MOON = '<svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 15A9 9 0 0 1 9 4a8 8 0 1 0 11 11Z"/></svg>'
BUTTON = f'<button class="theme-toggle" type="button" aria-label="Включить тёмную тему" title="Тёмная тема">{SUN}{MOON}</button>'

def patch(s):
    s = re.sub(r'/assets/theme\.(css|js)(\?v=\w+)?"', lambda m: f'/assets/theme.{m.group(1)}?v={THEME_VER}"', s)
    s = re.sub(r"<script>try\{if\(localStorage\.getItem\('itc-theme'\).*?</script>\s*", '', s, count=1, flags=re.S)
    s = re.sub(r'<html(?![^>]*data-theme)([^>]*)>', r'<html\1 data-theme="light">', s, count=1)
    s = s.replace('<head>', '<head>\n  ' + INLINE, 1)
    if '/assets/theme.css' not in s:
        s = s.replace('</head>', f'<link rel="stylesheet" href="/assets/theme.css?v={THEME_VER}"/>\n<script src="/assets/theme.js?v={THEME_VER}" defer></script>\n</head>', 1)
    s = re.sub(r'\s*<link rel="stylesheet" href="/assets/site.css[^"\n]*"/?>', '', s)
    s = s.replace('</head>', f'\n  <link rel="stylesheet" href="/assets/site.css?v={THEME_VER}"/>\n</head>', 1)
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    url = canonical.group(1) if canonical else ''
    services = '#directions' if url == 'https://itcompania.ru/' else '/#directions'
    works_active = ' class="is-active" aria-current="page"' if url.endswith('/portfolio/') else ''
    blog_active = ' class="is-active"' if '/blog/' in url else ''
    if url == 'https://itcompania.ru/blog/': blog_active += ' aria-current="page"'
    header = f'''<header>
  <a class="site-brand" href="/" aria-label="IT Компания — главная"><span class="site-brand-mark" aria-hidden="true"></span>IT Компания</a>
  <div class="site-navigation" role="navigation" aria-label="Основная навигация">
    <a href="{services}">Услуги</a><a href="/portfolio/"{works_active}>Работы</a><a href="/blog/"{blog_active}>Блог</a>
  </div>
  <div class="site-header-actions">{BUTTON}
    <a class="site-phone" href="tel:+79850249319" aria-label="Позвонить: +7 985 024-93-19"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 3h4l2 5-3 2a15 15 0 0 0 6 6l2-3 5 2v4c0 1-1 2-2 2A18 18 0 0 1 3 5c0-1 1-2 2-2Z"/></svg></a>
    <a class="btn-primary site-contact" href="https://t.me/manager379team" target="_blank" rel="noopener">Обсудить проект</a>
  </div>
</header>'''
    s = re.sub(r'<header[^>]*>.*?</header>', lambda m: header, s, count=1, flags=re.S)
    if '<main' not in s:
        s = s.replace('</header>', '</header>\n<main id="main-content">', 1)
        s = s.replace('<footer', '</main>\n<footer', 1)
    s = re.sub(r'(src="https://mc.yandex.ru/watch/[^\"]+"[^>]*)(?=alt="")', lambda m: m[1] if 'width=' in m[1] else m[1] + 'width="1" height="1" ', s)
    def external(m):
        tag = m.group(0)
        return tag if 'rel=' in tag else tag[:-1] + ' rel="noopener">'
    s = re.sub(r'<a\b[^>]*target="_blank"[^>]*>', external, s)
    return re.sub(r'[ \t]+\n', '\n', s)

def main():
    files = sorted(set(glob.glob(f'{ROOT}/*.html') + glob.glob(f'{ROOT}/*/index.html') + glob.glob(f'{ROOT}/blog/*/index.html')))
    changed = 0
    for f in files:
        if '/_tools/' in f or os.path.basename(f).startswith('yandex_'): continue
        s = open(f, encoding='utf-8').read()
        if '<html' not in s: continue
        n = patch(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n); changed += 1
    print(f'оформление: обновлено {changed} страниц')

if __name__ == '__main__': main()
