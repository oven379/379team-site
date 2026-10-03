# -*- coding: utf-8 -*-
"""Подключает светлую тему и переключатель ко всем страницам сайта. Повторный запуск безопасен.

Запуск из корня репозитория (после генераторов блога и страниц):
    python3 _tools/theme/apply_theme.py
"""
import glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

THEME_VER = '4'  # увеличивайте при правке assets/theme.css или theme.js
HEAD = ('<script>try{if(localStorage.getItem(\'itc-theme\')===\'light\')'
        'document.documentElement.setAttribute(\'data-theme\',\'light\')}catch(e){}</script>\n'
        f'  <link rel="stylesheet" href="/assets/theme.css?v={THEME_VER}"/>\n'
        f'  <script src="/assets/theme.js?v={THEME_VER}" defer></script>\n')

SUN = ('<svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8'
       'M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8L6 18M18 6l1.8-1.8"/></svg>')
MOON = ('<svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/></svg>')
BUTTON = f'<button class="theme-toggle" type="button" aria-label="Включить светлую тему" title="Светлая тема">{SUN}{MOON}</button>'


def patch(s):
    s = re.sub(r'/assets/theme\.(css|js)(\?v=\w+)?"', lambda m: f'/assets/theme.{m.group(1)}?v={THEME_VER}"', s)
    s = s.replace('<nav class="footer-nav" aria-label="Разделы сайта">', '<div class="footer-nav" role="navigation" aria-label="Разделы сайта">')
    s = re.sub(r'(<div class="footer-nav"[^>]*>.*?)</nav>', r'\1</div>', s, count=1, flags=re.S)
    if '/assets/theme.css' not in s:
        s = s.replace('</head>', '  ' + HEAD + '</head>', 1)
    # шапка: после ссылки «Блог»
    h = re.search(r'<header[^>]*>.*?</header>', s, re.S)
    if h and 'theme-toggle' not in h.group(0):
        new_h = re.sub(r'(>Блог</a>)', r'\1\n    ' + BUTTON.replace('\\', '\\\\'), h.group(0), count=1)
        s = s[:h.start()] + new_h + s[h.end():]
    # подвал: первой кнопкой в блоке с иконками
    f = re.search(r'<footer[^>]*>.*?</footer>', s, re.S)
    if f and 'theme-toggle' not in f.group(0):
        new_f = re.sub(r'(<div style="display:flex[^"]*">)', r'\1\n    ' + BUTTON.replace('\\', '\\\\'), f.group(0), count=1)
        s = s[:f.start()] + new_f + s[f.end():]
    # шапка: кнопка «Работы» перед «Блогом»
    h = re.search(r'<header[^>]*>.*?</header>', s, re.S)
    if h and 'href="/portfolio/" class="nav-pill' not in h.group(0):
        new_h = re.sub(r'(<a href="/blog/")', '<a href="/portfolio/" class="nav-pill">Работы</a>\n    \\1', h.group(0), count=1)
        s = s[:h.start()] + new_h + s[h.end():]
    # подвал: навигация после логотипа
    f = re.search(r'<footer[^>]*>.*?</footer>', s, re.S)
    if f and 'footer-nav' not in f.group(0):
        nav = ('\n  <div class="footer-nav" role="navigation" aria-label="Разделы сайта"><a href="/portfolio/">Работы</a>'
               '<a href="/blog/">Блог</a><a href="/usloviya-raboty/">Условия работы</a></div>')
        new_f = re.sub(r'(</a>|</span>)(\s*<div style="display:flex)', lambda m: m.group(1) + nav + m.group(2), f.group(0), count=1)
        s = s[:f.start()] + new_f + s[f.end():]
    # на странице портфолио кнопка «Работы» подсвечена
    if '<link rel="canonical" href="https://itcompania.ru/portfolio/"/>' in s:
        s = s.replace('<a href="/portfolio/" class="nav-pill">', '<a href="/portfolio/" class="nav-pill active" aria-current="page">', 1)
    return s


def main():
    files = sorted(set(glob.glob(f'{ROOT}/*.html') + glob.glob(f'{ROOT}/*/index.html') + glob.glob(f'{ROOT}/blog/*/index.html')))
    files = [f for f in files if '/_tools/' not in f and not os.path.basename(f).startswith('yandex_')]
    changed = 0
    for f in files:
        s = open(f, encoding='utf-8').read()
        if '<html' not in s:
            continue
        n = patch(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n); changed += 1
    print(f'тема: обновлено {changed} из {len(files)} страниц')


if __name__ == '__main__':
    main()
