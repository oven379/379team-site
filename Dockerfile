FROM nginx:alpine
COPY . /usr/share/nginx/html
# Конфиг nginx лежит в корне репозитория — переносим его из папки сайта в настройки
RUN mv /usr/share/nginx/html/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
