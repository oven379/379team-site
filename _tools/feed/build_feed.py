# -*- coding: utf-8 -*-
"""Собирает YML-фид услуг для Яндекс.Вебмастера (категория фида «Исполнители») и обложки услуг.

Запуск из корня репозитория:
    python3 _tools/feed/build_feed.py            # только /feed.yml
    python3 _tools/feed/build_feed.py --covers   # ещё и перерисовать обложки /feed/*.png (нужен Pillow)

Цены и названия — те же, что в карточках услуг на главной. Меняете цену на сайте — поменяйте и здесь.
Рейтинг, число отзывов и годы опыта задаются константами ниже — пишем только настоящие значения.
"""
import datetime, os, sys
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SITE = 'https://itcompania.ru'
NAME = 'It Компания'
EXPERIENCE_SINCE = 2019  # опыт команды, со слов владельца: 7 лет на 2026 год
RATING = 0                # отзывов пока нет; появятся настоящие — поставить средний балл
REVIEWS = 0
TELEGRAM = 'https://t.me/manager379team'
PHONE = 'tel:+79850249319'
REGION = 'Россия'
ABOUT = ('Студия разработки: сайты и интернет-магазины на Tilda, веб- и мобильные приложения, CRM, Telegram-боты. '
         'Работаем по договору, все доступы оформляем на клиента.')

# Категории — из списка Яндекса для фида «Исполнители»
CATEGORIES = [(1, None, 'Исполнитель'), (18, 1, 'Компьютеры и IT'), (19, 1, 'Дизайнеры')]
SETS = [('s1', 'Разработка сайтов, приложений и CRM — It Компания', SITE + '/')]

# slug страницы, название услуги, цена «от», за что цена, категория, описание
SERVICES = [
    ('lending', 'Лендинг на Tilda под ключ', 69000, 'за проект', 18,
     'Одностраничный сайт на Tilda: структура, тексты, дизайн, формы заявок, подключение аналитики.'),
    ('mnogostrannichny-sajt', 'Многостраничный сайт на Tilda', 99000, 'за проект', 18,
     'Сайт компании на Tilda: страницы услуг, портфолио, блог, формы заявок, базовая SEO-настройка.'),
    ('internet-magazin', 'Интернет-магазин на Tilda', 119000, 'за проект', 18,
     'Магазин на Tilda: каталог, корзина, онлайн-оплата, доставка, онлайн-касса.'),
    ('sajt-dlya-onlajn-shkoly', 'Сайт для онлайн-школы', 79000, 'за проект', 18,
     'Сайт курса или эксперта: программа, форма записи, приём оплаты, связка с платформой обучения.'),
    ('sajt-dlya-sellerov', 'Сайт для селлера маркетплейсов', 119000, 'за проект', 18,
     'Свой интернет-магазин для продавцов Ozon, Wildberries и Яндекс Маркета: каталог, оплата, доставка в пункты выдачи, касса.'),
    ('sajt-dlya-restorana', 'Сайт для ресторана и кафе', 69000, 'за проект', 18,
     'Сайт заведения на Tilda: меню с ценами, бронирование столика, заказ на доставку и самовывоз.'),
    ('sajt-dlya-proizvodstva', 'Сайт для производства и стройматериалов', 119000, 'за проект', 18,
     'Сайт производителя или поставщика: каталог продукции, прайс-лист, заявка на расчёт, условия доставки.'),
    ('detailing', 'Сайт для детейлинга и автосервиса', 39000, 'за проект', 18,
     'Готовый сайт для детейлинг-студии или автосервиса: услуги, цены, онлайн-запись, заявки в мессенджер.'),
    ('crm', 'Интеграция сайта с CRM', 29000, 'за проект', 18,
     'Подключение сайта к amoCRM или Битрикс24: заявки, воронка, уведомления, сквозная передача данных.'),
    ('busyclient', 'Сайт под ключ «Занятый клиент»', 89000, 'за проект', 18,
     'Сайт без участия заказчика: сами собираем материалы, пишем тексты, делаем дизайн и запускаем.'),
    ('socseti', 'Оформление социальных сетей', 19000, 'за проект', 19,
     'Оформление сообщества или канала: обложки, аватар, шаблоны постов в едином стиле.'),
    ('branding', 'Фирменный стиль и логотип', 49000, 'за проект', 19,
     'Логотип, цвета, шрифты и правила их использования: фирменный стиль для сайта и рекламы.'),
    ('seo', 'SEO-продвижение сайта на Tilda', 25000, 'в месяц', 18,
     'Продвижение сайта в Яндексе и Google: семантика, тексты, техническая настройка.'),
    ('razrabotka-veb-prilozhenij', 'Разработка веб-приложений', 250000, 'за спринт', 18,
     'Веб-сервисы, личные кабинеты и порталы на заказ: проектирование, разработка, тесты, запуск.'),
    ('devops', 'DevOps и поддержка серверов', 60000, 'в месяц', 18,
     'Настройка серверов, автоматическая выкладка, мониторинг и резервные копии для вашего продукта.'),
    ('razrabotka-crm-sistemy', 'Разработка CRM-системы', 250000, 'за спринт', 18,
     'CRM под процессы компании: заявки, клиенты, склад, отчёты, роли сотрудников, интеграции.'),
    ('telegram-boty', 'Разработка Telegram-ботов и Mini Apps', 50000, 'за проект', 18,
     'Чат-боты и мини-приложения Telegram: запись, заказы, оплата, уведомления, связка с CRM.'),
    ('razrabotka-sajta-na-zakaz', 'Разработка сайта на заказ', 250000, 'за спринт', 18,
     'Сайт на собственном коде, когда конструктора мало: сложная логика, интеграции, нестандартные задачи.'),
    ('mobile', 'Разработка мобильных приложений', 180000, 'за проект', 18,
     'Приложения для iOS и Android: проектирование, дизайн, разработка, публикация в магазинах.'),
]


def tag(name, value, attrs=''):
    return f'<{name}{attrs}>{escape(str(value))}</{name}>'


def build_feed():
    now = datetime.datetime.now()
    years = max(now.year - EXPERIENCE_SINCE, 1)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<yml_catalog date="{now.strftime("%Y-%m-%d %H:%M")}">', '  <shop>',
           '    ' + tag('name', NAME), '    ' + tag('company', NAME), '    ' + tag('url', SITE + '/'),
           '    <currencies>', '      <currency id="RUR" rate="1"/>', '    </currencies>', '    <categories>']
    for cid, parent, title in CATEGORIES:
        p = f' parentId="{parent}"' if parent else ''
        out.append(f'      <category id="{cid}"{p}>{escape(title)}</category>')
    out += ['    </categories>', '    <sets>']
    for sid, title, url in SETS:
        out += [f'      <set id="{sid}">', '        ' + tag('name', title), '        ' + tag('url', url), '      </set>']
    out += ['    </sets>', '    <offers>']
    for slug, title, price, unit, cat, text in SERVICES:
        url = f'{SITE}/{slug}/'
        assert os.path.exists(f'{ROOT}/{slug}/index.html'), f'нет страницы /{slug}/'
        assert os.path.exists(f'{ROOT}/feed/{slug}.png'), f'нет обложки /feed/{slug}.png — запустите с --covers'
        params = [('Рейтинг', RATING), ('Число отзывов', REVIEWS), ('Годы опыта', years), ('Регион', REGION), ('Конверсия', 1),
                  ('Организация', 'true'), ('Выполняется удаленно', 'true'),
                  ('Ссылка на чат', TELEGRAM), ('Ссылка на телефон', PHONE), ('Об исполнителе', ABOUT)]
        out += [f'      <offer id="{slug}">',
                '        ' + tag('name', NAME),
                '        ' + tag('url', url),
                '        ' + tag('price', price, ' from="true"'),
                '        ' + tag('currencyId', 'RUR'),
                '        ' + tag('sales_notes', unit),
                '        ' + tag('categoryId', cat),
                '        ' + tag('set-ids', ','.join(s[0] for s in SETS)),
                '        ' + tag('picture', f'{SITE}/feed/{slug}.png'),
                '        ' + tag('description', f'{title}. {text}')]
        out += ['        ' + tag('param', v, f' name="{k}"') for k, v in params]
        out.append('      </offer>')
    out += ['    </offers>', '  </shop>', '</yml_catalog>', '']
    open(f'{ROOT}/feed.yml', 'w', encoding='utf-8').write('\n'.join(out))
    print(f'фид: /feed.yml, услуг — {len(SERVICES)}')


def wrap(draw, text, font, width):
    lines, cur = [], ''
    for word in text.split():
        t = (cur + ' ' + word).strip()
        if draw.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = word
    return lines + [cur]


def build_covers():
    from PIL import Image, ImageDraw, ImageFont
    fonts = '/System/Library/Fonts/Supplemental/'
    bold = lambda size: ImageFont.truetype(fonts + 'Arial Bold.ttf', size)
    regular = lambda size: ImageFont.truetype(fonts + 'Arial.ttf', size)
    W = H = 800
    PAD, ACCENT, WHITE, MUTED = 72, '#b5e05a', '#f2f2f2', '#9a9a9a'
    os.makedirs(f'{ROOT}/feed', exist_ok=True)
    for slug, title, price, unit, cat, text in SERVICES:
        img = Image.new('RGB', (W, H), '#181818')
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 12, H], fill=ACCENT)
        d.text((PAD, 72), 'It', font=bold(36), fill=ACCENT)
        d.text((PAD + d.textlength('It ', font=bold(36)), 72), 'Компания', font=bold(36), fill=WHITE)
        size = 76
        while True:
            lines = wrap(d, title, bold(size), W - PAD * 2)
            widest = max(d.textlength(l, font=bold(size)) for l in lines)
            if (len(lines) <= 4 and widest <= W - PAD * 2) or size <= 44:
                break
            size -= 4
        y = 200
        for line in lines:
            d.text((PAD, y), line, font=bold(size), fill=WHITE)
            y += int(size * 1.18)
        money = f'{price:,}'.replace(',', ' ')
        d.text((PAD, 590), f'от {money} руб.', font=bold(52), fill=ACCENT)
        d.text((PAD + d.textlength(f'от {money} руб.  ', font=bold(52)), 608), unit, font=regular(32), fill=MUTED)
        d.text((PAD, 690), 'itcompania.ru', font=regular(32), fill=MUTED)
        img.save(f'{ROOT}/feed/{slug}.png', optimize=True)
    print(f'обложки: /feed/*.png, штук — {len(SERVICES)}')


if __name__ == '__main__':
    if '--covers' in sys.argv:
        build_covers()
    build_feed()
