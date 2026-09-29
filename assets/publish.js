/* Публикация статей блога по таймеру — без настроек сервера.
   Все статьи уже лежат на сайте; этот скрипт показывает их посетителям в дату выхода в 10:00 по Москве.
   data-publish="ГГГГ-ММ-ДД" — элемент появляется в эту дату (до неё скрыт стилями).
   <a data-publish data-inline> — ссылка внутри текста: до даты показывается обычным текстом.
   [data-list="3"] — показать не больше 3 вышедших элементов; если ни одного — скрыть блок.
   <html data-gate="ГГГГ-ММ-ДД"> — страница статьи: до даты вместо текста показывается «Статья выйдет …». */
(function () {
  var now = new Date();
  function at(d) { return new Date(d + 'T10:00:00+03:00'); }
  function live(el) { return at(el.getAttribute('data-publish')) <= now; }

  document.querySelectorAll('a[data-publish][data-inline]').forEach(function (a) {
    if (!live(a)) { var s = document.createElement('span'); s.innerHTML = a.innerHTML; a.replaceWith(s); }
  });

  document.querySelectorAll('[data-list]').forEach(function (list) {
    var max = parseInt(list.getAttribute('data-list'), 10) || 999, shown = 0;
    list.querySelectorAll(':scope > [data-publish]').forEach(function (el) {
      if (live(el) && shown < max) { el.removeAttribute('data-publish'); shown++; }
    });
    if (!shown) { var box = list.closest('[data-list-box]'); if (box) box.style.display = 'none'; }
  });

  document.querySelectorAll('[data-publish]:not([data-inline])').forEach(function (el) {
    if (!el.closest('[data-list]') && live(el)) el.removeAttribute('data-publish');
  });

  var gate = document.documentElement.getAttribute('data-gate');
  if (gate) {
    var msg = document.getElementById('gate-msg');
    var tick = function () {
      var ms = at(gate) - new Date();
      if (ms <= 0) { document.documentElement.classList.remove('gated'); return; }
      var d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
      if (msg) msg.textContent = 'До выхода: ' + d + ' дн. ' + h + ' ч ' + m + ' мин';
      setTimeout(tick, 30000);
    };
    tick();
  }
})();
