#!/bin/sh

echo DEBUG=0 >> .env
echo SQL_ENGINE=django.db.backends.postgresql >> .env
echo DATABASE=postgres >> .env

echo POSTGRES_DATABASE_NAME=${{ secrets.SQL_DATABASE }} >> .env
echo POSTGRES_USER=${{ secrets.SQL_USER }} >> .env
echo POSTGRES_PASSWORD=${{ secrets.SQL_PASSWORD }} >> .env
echo POSTGRES_HOST=${{ secrets.SQL_HOST }} >> .env
echo POSTGRES_PORT=5432 >> .env