FROM nginx:1.19.7-alpine

RUN apk add --no-cache bash certbot certbot-nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY start.sh /app/start.sh

WORKDIR /app

RUN touch /var/run/nginx.pid

RUN chmod +x /app/start.sh

USER root

CMD ["/app/start.sh"]

