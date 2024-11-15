# payment-analysis
Автоматизация разбора платежей.

## Запуск скрипта в докер-контейнере

```
Переименовать файл .env.example в .env
```

```
cd ./script
```

```
docker build --tag 'script' .
```

```
docker run --rm -v ${pwd}/data:/opt/app/data --env-file .env 'script'
```
