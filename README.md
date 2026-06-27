# 379TEAM — Инструкция по запуску

## Локальный просмотр

### Через Python (самый простой способ):
1. Положи оба файла (index.html и llms.txt) в одну папку
2. Открой терминал в этой папке
3. Выполни команду:

```bash
python3 -m http.server 8080
```

4. Открой браузер: http://localhost:8080
5. llms.txt будет доступен: http://localhost:8080/llms.txt

### Через Node.js:
```bash
npx serve .
```

---

## Размещение на REG.RU (хостинг)

1. Зайди в REG.RU → Хостинг → Файловый менеджер
2. Перейди в папку public_html
3. Загрузи оба файла: index.html и llms.txt
4. Сайт будет доступен по твоему домену
5. llms.txt будет по адресу: https://твойдомен.ru/llms.txt

---

## Размещение на VPS/сервере (Nginx)

1. Скопируй файлы на сервер:
```bash
scp index.html llms.txt user@твой_сервер:/var/www/html/
```

2. Настрой Nginx (/etc/nginx/sites-available/default):
```nginx
server {
    listen 80;
    server_name твойдомен.ru www.твойдомен.ru;
    root /var/www/html;
    index index.html;

    location /llms.txt {
        add_header Content-Type "text/plain; charset=utf-8";
        try_files /llms.txt =404;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

3. Перезапусти Nginx:
```bash
sudo nginx -s reload
```

---

## Проверка после размещения

Зайди на https://signum.ai/ai-checker/ и проверь свой домен.
Должно стать: обнаружение llms.txt — 15/15 ✓
