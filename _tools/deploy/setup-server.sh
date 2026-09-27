#!/bin/sh
# Однократная настройка сервера itcompania.ru. Запускать от root:
#   curl -fsSL https://raw.githubusercontent.com/oven379/379team-site/main/_tools/deploy/setup-server.sh -o /root/setup-site.sh
#   sh /root/setup-site.sh
#
# Что делает (и останавливается при любой неожиданности, ничего не сломав):
#   1. находит настройки nginx и папку сайта itcompania.ru;
#   2. проверяет, что на сервере нет своих изменений, которых нет на GitHub;
#   3. делает резервные копии папки сайта и настроек nginx;
#   4. обновляет сайт до версии с GitHub и собирает блог;
#   5. в nginx: закрывает .git и служебные файлы, включает настоящую страницу 404;
#   6. ставит автообновление каждые 10 минут (cron).
# Повторный запуск безопасен.
set -eu

say()  { printf '\n== %s\n' "$*"; }
fail() { printf '\n!! %s\n\n' "$*"; exit 1; }
STAMP=$(date +%Y%m%d-%H%M)

[ "$(id -u)" = 0 ] || fail "Запустите от root (или через sudo)."
command -v git >/dev/null     || fail "На сервере нет git."
command -v python3 >/dev/null || fail "На сервере нет python3. Установите: apt install -y python3"

say "1. Ищу настройки nginx для itcompania.ru"
CONF=$(grep -rlE 'server_name[^;]*itcompania\.ru' /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null | head -n 1 || true)
[ -n "$CONF" ] || fail "Не нашёл настройки nginx с itcompania.ru. Пришлите вывод команды: grep -rn server_name /etc/nginx/"
CONF=$(readlink -f "$CONF")
SITE=$(grep -E '^[[:space:]]*root[[:space:]]' "$CONF" | head -n 1 | awk '{print $2}' | tr -d ';')
[ -n "$SITE" ] && [ -d "$SITE/.git" ] || fail "Папка сайта ($SITE) не является копией репозитория GitHub."
echo "настройки nginx: $CONF"
echo "папка сайта:     $SITE"

say "2. Проверяю, нет ли на сервере своих изменений"
git config --global --add safe.directory "$SITE" 2>/dev/null || true
cd "$SITE"
git fetch -q origin main
EDITED=$(git status --porcelain --untracked-files=no)
UNIQUE=$(git diff --stat origin/main...HEAD)
if [ -n "$EDITED$UNIQUE" ]; then
  echo "$EDITED"; echo "$UNIQUE"
  fail "На сервере есть изменения, которых нет на GitHub. Ничего не менял — пришлите этот вывод."
fi
echo "своих изменений нет"

say "3. Резервные копии"
cp -a "$SITE" "$SITE.backup-$STAMP"
cp "$CONF" "/root/nginx-itcompania.conf.backup-$STAMP"
echo "сайт:  $SITE.backup-$STAMP"
echo "nginx: /root/nginx-itcompania.conf.backup-$STAMP"

say "4. Обновляю сайт до версии с GitHub"
git reset -q --hard origin/main
python3 _tools/blog/build_blog.py
git log -1 --format='версия: %h %s'

say "5. Настраиваю nginx"
python3 - "$CONF" <<'PY'
import re, sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
MARK = '# itcompania-deploy'
if MARK not in s:
    rule = ('\n    ' + MARK + ': служебные файлы не отдаём (кроме .well-known для SSL), настоящая страница 404\n'
            '    location ~ (^/\\.(?!well-known/)|^/_tools/|^/Dockerfile$|^/nginx\\.conf$) { return 404; }\n'
            '    error_page 404 /404.html;\n')
    s, n = re.subn(r'(^[ \t]*root[ \t]+[^;]+;[ \t]*\n)', lambda m: m.group(1) + rule, s, flags=re.M)
    if not n:
        sys.exit('не нашёл строку root в настройках nginx')
# несуществующие адреса — 404, а не главная страница
s = s.replace('try_files $uri $uri/ /index.html;', 'try_files $uri $uri/ =404;')
open(path, 'w', encoding='utf-8').write(s)
print('правила добавлены')
PY
if nginx -t 2>/tmp/nginx-test.log; then
  systemctl reload nginx
  echo "nginx перезагружен"
else
  cat /tmp/nginx-test.log
  cp "/root/nginx-itcompania.conf.backup-$STAMP" "$CONF"
  fail "nginx не принял настройки — вернул прежние. Пришлите этот вывод."
fi

say "6. Автообновление каждые 10 минут"
JOB="*/10 * * * * sh $SITE/_tools/deploy/update-site.sh >> /var/log/itcompania-update.log 2>&1"
( crontab -l 2>/dev/null | grep -v 'itcompania-update' || true; echo "$JOB" ) | crontab -
echo "$JOB"

say "Проверка"
for u in / /blog/ /.git/config /_tools/blog/README.md /nesuschestvuet/; do
  printf '%-26s %s\n' "$u" "$(curl -s -o /dev/null -w '%{http_code}' "https://itcompania.ru$u" || echo ошибка)"
done
echo
echo "Ожидается: /  и /blog/ — 200, остальные — 404."
echo "Готово. Дальше сайт обновляется сам через 10 минут после Push на GitHub."
