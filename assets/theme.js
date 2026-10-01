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
