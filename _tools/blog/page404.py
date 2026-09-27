# -*- coding: utf-8 -*-
# Подключается в конце build_blog.py: собирает /404.html в стиле сайта.

def build_404():
    page = head('Страница не найдена | It Компания',
                'Такой страницы нет на сайте It Компании. Перейдите на главную, в блог или к услугам.',
                'https://itcompania.ru/404.html', 'website', [])
    # 404 не должна попадать в поиск и не должна подсвечивать «Блог» как текущий раздел
    page = page.replace('<meta name="robots" content="index, follow, max-image-preview:large"/>',
                        '<meta name="robots" content="noindex, follow"/>')
    page = page.replace('  <link rel="canonical" href="https://itcompania.ru/404.html"/>\n', '')
    page = page.replace('<a href="/blog/" class="blog-link active" aria-current="page">', '<a href="/blog/" class="blog-link">')
    page += '''
<div class="hero" style="min-height:52vh">
  <p class="eyebrow">Ошибка 404</p>
  <h1>Такой страницы <em>нет</em></h1>
  <p class="hero-sub">Возможно, адрес набран с ошибкой или страница переехала. Вот куда можно перейти:</p>
  <div class="hero-actions">
    <a class="btn-primary" href="/">На главную</a>
    <a class="btn-ghost" href="/blog/">Блог</a>
    <a class="btn-ghost" href="/#services">Все услуги</a>
  </div>
  <p class="meta">Искали что-то конкретное? Напишите нам в <a href="''' + TG + '''" target="_blank" rel="noopener" style="color:var(--accent)">Telegram</a> — подскажем.</p>
</div>
''' + TAIL
    open(f'{ROOT}/404.html', 'w').write(add_metrika(page))

build_404()
print('404 ok')
