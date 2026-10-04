# -*- coding: utf-8 -*-
# Проекты для портфолио и блоков «Примеры работ» на страницах услуг.
# Один проект описывается один раз; tags — на каких страницах услуг его показывать.
# confirmed=False — проект не выводится, пока владелец не подтвердит, что это наша работа.

APPS = [
    dict(
        name='КарПас', kind='Мобильное приложение + CRM + веб',
        text='Цифровая история обслуживания авто для владельцев и CRM для детейлингов и СТО. iOS, Android и веб, 3 месяца разработки и тестов.',
        appstore='https://apps.apple.com/ru/app/carpasss-%D0%BA%D0%B0%D1%80%D0%BF%D0%B0%D1%81%D1%81%D1%81/id6768924960',
        site='https://carpasss.ru', case='/blog/keis-karpas/',
        tags=['mobile', 'crm-dev', 'webapp'], confirmed=True,
    ),
    dict(
        name='ДелайДело', kind='Мобильное приложение',
        text='Планировщик задач на день: напоминания, перенос дел на завтра, календарь планов, тёмная и светлая тема. Без рекламы и регистрации.',
        appstore='https://apps.apple.com/us/app/%D0%B4%D0%B5%D0%BB%D0%B0%D0%B9%D0%B4%D0%B5%D0%BB%D0%BE/id6759549338?l=ru',
        site='https://delodelai.ru',
        tags=['mobile'], confirmed=True,
    ),
    dict(
        name='Агрологистика', kind='Мобильное приложение для бизнеса',
        text='Поиск заявок на перевозку с фильтрами, отклик на заявку в одно нажатие, личный кабинет с документами. Работали над приложением с момента запуска проекта.',
        appstore='https://apps.apple.com/ru/app/%D0%B0%D0%B3%D1%80%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0/id6743162740',
        site='https://agrozernovoz.ru',
        tags=['mobile', 'webapp'], confirmed=True,
    ),
    dict(
        name='Моднова', kind='Мобильное приложение',
        text='Личный кабинет участника программы лояльности сети магазинов «Моднова» в смартфоне. Работали над приложением с момента запуска проекта.',
        appstore='https://apps.apple.com/ru/app/%D0%BC%D0%BE%D0%B4%D0%BD%D0%BE%D0%B2%D0%B0/id6751570834',
        tags=['mobile'], confirmed=True,
    ),
]

# Сайты: только те, что открываются (проверено 29.09.2026). tilda=False — сделан не на Tilda.
SITES = [
    dict(name='Magertrade', niche='Насосы и насосное оборудование, каталог', url='https://magertrade.ru', tilda=True, tags=['factory']),
    dict(name='MetaRacing', niche='Клубы гоночных симуляторов, Москва и Санкт-Петербург', url='https://metaracing.ru', tilda=False),
    dict(name='Батист', niche='Премиальный салон штор', url='https://batist-dn.ru', tilda=False),
    dict(name='Terricon City', niche='Тротуарная плитка и бордюры', url='https://terriconcity.ru', tilda=True, tags=['factory']),
    dict(name='Базис Строй', niche='Тротуарная плитка, бордюры, шлакоблок', url='https://bazisstroydn.ru', tilda=True, tags=['factory']),
    dict(name='Полезно', niche='Программы сопровождения по питанию', url='https://poleznolife.ru', tilda=True, tags=['course']),
    dict(name='Neprostoidea', niche='Системы управления процессами и проектами', url='https://neprostoidea.com', tilda=True),
    dict(name='ТИК', niche='Системы безопасности для квартир и бизнеса', url='https://tikdn.ru', tilda=True),
    dict(name='Товарищ Сухов', niche='Ресторан восточной кухни', url='https://suhowdn.ru', tilda=True, tags=['restaurant']),
    dict(name='Cafe City', niche='Кафе и доставка еды', url='https://cafe-city-sh.ru', tilda=True, tags=['restaurant']),
    dict(name='A-Lion', niche='Автосервис Peugeot, Renault, Citroen', url='https://a-lion.ru', tilda=True),
    dict(name='Mobysound', niche='Аренда звукового и светового оборудования', url='https://mobysound.ru', tilda=True),
    dict(name='Venditore', niche='Кофе и кофейное оборудование', url='https://venditoredn.ru', tilda=True),
    dict(name='Мастер-Замки', niche='Срочное вскрытие замков 24/7', url='https://master-zamkidn.ru', tilda=True),
    dict(name='Виктория Гизатуллина', niche='Сайт-портфолио художника', url='https://gizatullinaart.ru', tilda=True),
    dict(name='Нефтегазовое оборудование', niche='Проект на Behance', url='https://www.behance.net/gallery/232205811/neftegazovoe-oborudovanie', tilda=True, behance=True),
]

# Кейсы с подробным разбором (показываются первыми в портфолио и на страницах услуг по tags)
PROJECTS = [
    dict(
        name='AlphaPride', kind='Сайт компании + интернет-магазин на Tilda',
        text='Дистрибьютор спортивного питания GEON: корпоративный сайт и магазин. Доставка Ozon в пункты выдачи прямо в корзине, оплата картой и по счёту для юрлиц, онлайн-касса.',
        site='https://alphapride.ru/market', case='/blog/keis-alphapride/',
        tags=['shop'], confirmed=True,
    ),
]
