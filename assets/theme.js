/* Переключатель светлой/тёмной темы. Тема ставится до отрисовки маленьким скриптом в <head>
   (без мигания), а этот файл обрабатывает нажатия и запоминает выбор. */
(function () {
  var KEY = 'itc-theme';
  function apply(theme, save) {
    var light = theme === 'light';
    if (light) document.documentElement.setAttribute('data-theme', 'light');
    else document.documentElement.removeAttribute('data-theme');
    if (save) { try { localStorage.setItem(KEY, theme); } catch (e) {} }
    document.querySelectorAll('.theme-toggle').forEach(function (b) {
      b.setAttribute('aria-label', light ? 'Включить тёмную тему' : 'Включить светлую тему');
      b.setAttribute('title', light ? 'Тёмная тема' : 'Светлая тема');
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.theme-toggle');
    if (!b) return;
    apply(document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light', true);
  });
  apply(document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark', false);
})();

/* Уведомление о cookie. Выбор хранится в браузере (itc-cookies: yes / no) и больше не спрашивается.
   При отказе Яндекс Метрика отключается маленьким скриптом в <head> на следующих страницах. */
(function () {
  var KEY = 'itc-cookies', choice = null;
  try { choice = localStorage.getItem(KEY); } catch (e) { return; }
  if (choice) return;
  function show() {
    var box = document.createElement('div');
    box.className = 'cookie-bar';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Уведомление о файлах cookie');
    box.innerHTML = '<p>Сайт использует файлы cookie и Яндекс Метрику, чтобы понимать, как им пользуются, и становиться удобнее.</p>' +
      '<div class="cookie-bar__btns"><button type="button" class="cookie-bar__no">Отклонить</button>' +
      '<button type="button" class="cookie-bar__yes">Разрешить</button></div>';
    document.body.appendChild(box);
    function done(value) {
      try { localStorage.setItem(KEY, value); } catch (e) {}
      if (value === 'no') window['disableYaCounter113101565'] = true;
      box.remove();
    }
    box.querySelector('.cookie-bar__yes').addEventListener('click', function () { done('yes'); });
    box.querySelector('.cookie-bar__no').addEventListener('click', function () { done('no'); });
  }
  if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
})();
