FROM node:23.11.1-alpine as fr

RUN npm config set registry https://registry.npm.taobao.org/

WORKDIR /app

COPY fr/package.json /app/
COPY fr/package-lock.json /app/

RUN npm i

COPY fr/. /app/

RUN npm run build

EXPOSE 5173


FROM python:3.12.10-alpine

RUN apk add --update caddy gcc musl-dev libffi-dev

WORKDIR /app

COPY ba/requirements.txt /app/

RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN pip3 install -r requirements.txt

COPY ba/. /app/

COPY Caddyfile /app/Caddyfile

COPY --from=fr /app/dist /app/backend/dist

EXPOSE 80

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]