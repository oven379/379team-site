# -*- coding: utf-8 -*-
# Подключается в конце build_blog.py: собирает страницу /admin/ — расписание публикаций с таймером.
# Сервер не настраивается, поэтому вход проверяется в браузере: в коде хранится только хеш пароля.
# Это «занавеска» от случайных посетителей, а не защита: на странице нет ничего секретного.
# Сменить пароль: printf '%s' 'itcompania-admin:НОВЫЙ_ПАРОЛЬ' | shasum -a 256  → вставить в ADMIN_HASH.

ADMIN_HASH = 'd0a07c0448108642e3776ef004b9891fc92551e38ae338a3dabf6fddee8a4c4c'
GITHUB_EDIT = 'https://github.com/oven379/379team-site/edit/main/_tools/blog/posts_plan.py'

def build_admin():
    items = sorted(ALL_POSTS, key=lambda p: p['date'])
    data = [{'slug': p['slug'], 'title': p['h1'], 'date': p['date'], 'date_h': p['date_h']} for p in items]
    rows = ''.join(f'\n    <tr data-date="{p["date"]}"><td>{p["date_h"]}, 10:00</td><td class="st">—</td>'
                   f'<td><a href="/blog/{p["slug"]}/" target="_blank">{p["h1"]}</a></td></tr>' for p in items)
    page = head('Расписание публикаций — админка', 'Служебная страница.', 'https://itcompania.ru/admin/', 'website', [])
    page = page.replace('<meta name="robots" content="index, follow, max-image-preview:large"/>',
                        '<meta name="robots" content="noindex, nofollow"/>')
    page = page.replace('  <link rel="canonical" href="https://itcompania.ru/admin/"/>\n', '')
    page = page.replace('<a href="/blog/" class="blog-link active" aria-current="page">', '<a href="/blog/" class="blog-link">')
    page += f'''
<div class="hero" id="login" style="max-width:520px">
  <p class="eyebrow">Админка блога</p>
  <h1>Вход</h1>
  <form id="login-form" autocomplete="off">
    <input id="pass" type="password" inputmode="numeric" placeholder="Пароль" aria-label="Пароль"
      style="width:100%;padding:14px 16px;border-radius:8px;border:1px solid var(--border);background:var(--bg2);color:var(--text);font-size:16px;margin-bottom:12px"/>
    <button class="btn-primary" type="submit" style="border:0;cursor:pointer">Войти</button>
    <p class="meta" id="login-err" style="margin-top:12px"></p>
  </form>
</div>

<div id="panel" hidden>
<div class="hero" style="padding-bottom:24px">
  <p class="eyebrow">Админка блога</p>
  <h1>Расписание <em>публикаций</em></h1>
  <p class="hero-sub" id="next">Следующая статья: считаем…</p>
  <p class="meta">Статьи уже лежат на сайте и открываются посетителям сами в свою дату в 10:00 по Москве.</p>
</div>

<section style="padding-top:0">
  <div class="table-wrap"><table class="admin">
    <thead><tr><th>Выход</th><th>Статус</th><th>Статья</th></tr></thead>
    <tbody>{rows}
    </tbody>
  </table></div>

  <h2 style="margin-top:48px">Как перенести статью или опубликовать раньше</h2>
  <ol class="admin-help">
    <li>Напишите Claude, какую статью и на какую дату перенести, — он поменяет расписание и пересоберёт сайт. Или сами откройте <a href="{GITHUB_EDIT}" target="_blank" rel="noopener">список статей на GitHub</a> и поменяйте у статьи строки <code>date</code> и <code>date_h</code>.</li>
    <li>После изменения сайт нужно пересобрать и выгрузить на сервер — так же, как при любом обновлении сайта.</li>
  </ol>
  <p class="meta">Новые статьи и правки текстов удобнее всего присылать Claude: он напишет, проверит и поставит в расписание.</p>
</section>
</div>

<style>
  .admin{{width:100%;border-collapse:collapse;font-size:15px}}
  .admin th{{background:var(--bg3);text-align:left;padding:12px 14px;color:var(--white)}}
  .admin td{{padding:12px 14px;border-top:1px solid var(--border);color:#d6d6d6;vertical-align:top}}
  .admin a{{color:var(--text)}}
  .admin tr.live .st{{color:var(--accent)}}
  .admin tr.next{{background:rgba(181,224,90,.06)}}
  .admin-help{{margin:12px 0 16px 22px;color:#d6d6d6;line-height:1.8}}
  .admin-help a{{color:var(--accent)}}
  .admin-help code{{background:var(--bg3);border-radius:4px;padding:1px 6px}}
  .table-wrap{{overflow-x:auto;border:1px solid var(--border);border-radius:10px}}
</style>
<script>
(function(){{
  var HASH = '{ADMIN_HASH}';
  var posts = {json.dumps(data, ensure_ascii=False)};
  async function sha(s){{
    var b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
    return Array.from(new Uint8Array(b)).map(function(x){{ return x.toString(16).padStart(2,'0'); }}).join('');
  }}
  function open(){{ document.getElementById('login').hidden = true; document.getElementById('panel').hidden = false; tick(); setInterval(tick, 1000); }}
  try {{ if (sessionStorage.getItem('itc-admin') === HASH) open(); }} catch(e) {{}}
  document.getElementById('login-form').addEventListener('submit', async function(e){{
    e.preventDefault();
    var h = await sha('itcompania-admin:' + document.getElementById('pass').value);
    if (h === HASH) {{ try {{ sessionStorage.setItem('itc-admin', HASH); }} catch(e) {{}} open(); }}
    else document.getElementById('login-err').textContent = 'Неверный пароль';
  }});
  var at = function(d){{ return new Date(d + 'T10:00:00+03:00'); }};
  function tick(){{
    var now = new Date(), next = null, rows = document.querySelectorAll('.admin tbody tr');
    rows.forEach(function(r){{
      var live = at(r.dataset.date) <= now;
      r.classList.toggle('live', live);
      r.querySelector('.st').textContent = live ? 'вышла' : 'ждёт';
      if (!live && !next) next = r;
    }});
    rows.forEach(function(r){{ r.classList.toggle('next', r === next); }});
    var el = document.getElementById('next');
    if (!next) {{ el.textContent = 'Все запланированные статьи вышли. Пора подготовить новые.'; return; }}
    var p = posts.filter(function(x){{ return x.date === next.dataset.date; }})[0];
    var ms = at(p.date) - now, d = Math.floor(ms/864e5), h = Math.floor(ms%864e5/36e5), m = Math.floor(ms%36e5/6e4), s = Math.floor(ms%6e4/1e3);
    el.textContent = 'Следующая статья «' + p.title + '» выйдет ' + p.date_h + ' в 10:00 — через ' + d + ' дн. ' + h + ' ч ' + m + ' мин ' + s + ' с';
  }}
}})();
</script>
''' + TAIL
    os.makedirs(f'{ROOT}/admin', exist_ok=True)
    open(f'{ROOT}/admin/index.html', 'w', encoding='utf-8').write(page)

build_admin()
print('админка: /admin/')
