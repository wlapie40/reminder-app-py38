FROM nginx:1.17-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
#COPY static/ /etc/nginx/html/static/
#COPY cert.pem /etc/nginx/cert.pem
#COPY key.pem /etc/nginx/key.pem