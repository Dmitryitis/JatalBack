FROM node:14-alpine as node

WORKDIR /app

COPY package.json .
COPY package-lock.json .
RUN npm ci --no-optional

COPY src/static/ /app/src/static/
COPY gulpfile.js .
RUN npm run build

FROM python:3.9.5-alpine

WORKDIR /app
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache bash postgresql-libs postgresql-dev g++ gcc libxslt-dev jpeg-dev zlib-dev linux-headers

COPY requirements.txt .
RUN pip install -r requirements.txt && pip install uwsgi==2.0.19.1
COPY wait-for-it.sh .
COPY . .

COPY --from=node /app/src/static/ /app/src/static/

RUN python3 src/manage.py collectstatic --noinput

ENV DEBUG False
ENV SENTRY_ENVIRONMENT staging

EXPOSE 5000

CMD python src/manage.py migrate
