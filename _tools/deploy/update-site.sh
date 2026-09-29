#!/bin/sh
# Автообновление сайта itcompania.ru на сервере.
# Запускается cron каждые 10 минут (ставит setup-server.sh):
#   1) забирает последнюю версию с GitHub (ветка main);
#   2) пересобирает блог — статьи выходят сами в свою дату в 10:00 по Москве.
# Правки, сделанные прямо на сервере, будут перезаписаны: сайт меняем только через GitHub.
set -eu

SITE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$SITE_DIR"

git fetch -q origin main
git reset -q --hard origin/main
python3 _tools/blog/build_blog.py > /dev/null
python3 _tools/pages/build_pages.py > /dev/null
