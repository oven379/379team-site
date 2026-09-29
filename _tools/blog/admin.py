# -*- coding: utf-8 -*-
# Подключается в конце build_blog.py: собирает закрытую страницу /admin/ — расписание публикаций.
# Страница не индексируется, не попадает в sitemap и в git (.gitignore); на сервере закрыта паролем (nginx).

GITHUB_EDIT = 'https://github.com/oven379/379team-site/edit/main/_tools/blog/posts_plan.py'
GITHUB_EDIT_OLD = 'https://github.com/oven379/379team-site/edit/main/_tools/blog/posts.py'

def build_admin():
    items = sorted(ALL_POSTS, key=lambda p: p['date'])
    data = [{'slug': p['slug'], 'title': p['h1'], 'date': p['date'], 'date_h': p['date_h']} for p in items]
    built = NOW_MSK.strftime('%d.%m.%Y %H:%M')
    rows = ''
    for p in items:
        live = p in POSTS
        link = f'<a href="/blog/{p["slug"]}/" target="_blank">{p["h1"]}</a>' if live else p['h1']
        rows += (f'\n    <tr data-date="{p["date"]}"><td>{p["date_h"]}, 10:00</td>'
                 f'<td class="st">{"вышла" if live else "ждёт"}</td><td>{link}</td></tr>')
    page = head('Расписание публикаций — админка', 'Служебная страница.', 'https://itcompania.ru/admin/', 'website', [])
    page = page.replace('<meta name="robots" content="index, follow, max-image-preview:large"/>',
                        '<meta name="robots" content="noindex, nofollow"/>')
    page = page.replace('  <link rel="canonical" href="https://itcompania.ru/admin/"/>\n', '')
    page = page.replace('<a href="/blog/" class="blog-link active" aria-current="page">', '<a href="/blog/" class="blog-link">')
    page += f'''
<div class="hero" style="padding-bottom:24px">
  <p class="eyebrow">Админка блога</p>
  <h1>Расписание <em>публикаций</em></h1>
  <p class="hero-sub" id="next">Следующая статья: считаем…</p>
  <p class="meta" id="built">Сайт обновлён с GitHub: {built} по Москве</p>
</div>

<section style="padding-top:0">
  <div class="table-wrap"><table class="admin">
    <thead><tr><th>Выход</th><th>Статус</th><th>Статья</th></tr></thead>
    <tbody>{rows}
    </tbody>
  </table></div>

  <h2 style="margin-top:48px">Как опубликовать раньше или перенести статью</h2>
  <ol class="admin-help">
    <li>Откройте <a href="{GITHUB_EDIT}" target="_blank" rel="noopener">список статей на GitHub</a> (для первых пяти статей — <a href="{GITHUB_EDIT_OLD}" target="_blank" rel="noopener">этот файл</a>).</li>
    <li>Найдите статью по названию и поменяйте две строки: <code>date='ГГГГ-ММ-ДД'</code> и <code>date_h='день месяц год'</code>. Чтобы опубликовать сразу — поставьте сегодняшнюю дату (статья выйдет, если сейчас уже больше 10:00 по Москве).</li>
    <li>Нажмите зелёную кнопку <b>Commit changes</b>.</li>
    <li>Через 10 минут сайт обновится сам. Проверьте статус на этой странице.</li>
  </ol>
  <p class="meta">Новые статьи и правки текстов проще присылать Claude: он напишет, проверит и поставит в расписание.</p>
</section>

<style>
  .admin{{width:100%;border-collapse:collapse;font-size:15px}}
  .admin th{{background:var(--bg3);text-align:left;padding:12px 14px;color:var(--white)}}
  .admin td{{padding:12px 14px;border-top:1px solid var(--border);color:#d6d6d6;vertical-align:top}}
  .admin a{{color:var(--accent)}}
  .admin tr.live .st{{color:var(--accent)}}
  .admin tr.next{{background:rgba(200,255,0,.06)}}
  .admin-help{{margin:12px 0 16px 22px;color:#d6d6d6;line-height:1.8}}
  .admin-help a{{color:var(--accent)}}
  .admin-help code{{background:var(--bg3);border-radius:4px;padding:1px 6px}}
  .table-wrap{{overflow-x:auto;border:1px solid var(--border);border-radius:10px}}
  #built.stale{{color:#ff6b6b}}
</style>
<script>
(function(){{
  var posts = {json.dumps(data, ensure_ascii=False)};
  var at = function(d){{ return new Date(d + 'T10:00:00+03:00'); }};
  var rows = document.querySelectorAll('.admin tbody tr');
  var built = '{NOW_MSK.isoformat()}';
  function tick(){{
    var now = new Date(), next = null;
    rows.forEach(function(r){{
      var live = at(r.dataset.date) <= now;
      r.classList.toggle('live', live);
      if (!live && !next) next = r;
    }});
    rows.forEach(function(r){{ r.classList.toggle('next', r === next); }});
    var el = document.getElementById('next');
    if (!next) {{ el.textContent = 'Все запланированные статьи вышли. Пора составить новый план.'; }}
    else {{
      var p = posts.filter(function(x){{ return x.date === next.dataset.date; }})[0];
      var ms = at(p.date) - now, d = Math.floor(ms/864e5), h = Math.floor(ms%864e5/36e5), m = Math.floor(ms%36e5/6e4), s = Math.floor(ms%6e4/1e3);
      el.textContent = 'Следующая статья «' + p.title + '» выйдет ' + p.date_h + ' в 10:00 — через ' + d + ' дн. ' + h + ' ч ' + m + ' мин ' + s + ' с';
    }}
    var b = document.getElementById('built');
    var stale = (now - new Date(built)) > 30*60*1000;
    b.classList.toggle('stale', stale);
    if (stale) b.textContent = 'Сайт обновлён с GitHub: {built} по Москве — больше 30 минут назад. Автообновление на сервере не работает, проверьте журнал /var/log/itcompania-update.log';
  }}
  tick(); setInterval(tick, 1000);
}})();
</script>
''' + TAIL
    os.makedirs(f'{ROOT}/admin', exist_ok=True)
    open(f'{ROOT}/admin/index.html', 'w', encoding='utf-8').write(page)

build_admin()
print('админка: /admin/')
