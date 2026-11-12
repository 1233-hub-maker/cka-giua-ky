FROM nginx:1.27-alpine
ARG APP_VERSION=v1
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
RUN sed -i "s/__FRONTEND_VERSION__/${APP_VERSION}/" /usr/share/nginx/html/index.html
EXPOSE 80
