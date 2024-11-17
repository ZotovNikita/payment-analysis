# payment-analysis
Автоматизация разбора платежей.

## Запуск скрипта в докер-контейнере

Для теста необходимо заменить файл `script/data/payments_main.tsv` на Ваш контрольный файл.

После запуска скрипта в контейнере рядом с каждый файлом `.tsv` в папке `script/data/` будет сгенерирован файл с ответами (например, для файла `script/data/{название}.tsv` будет сгенерирован файл `script/data/{название}_predicted.tsv`)

1. Перейдите в папку `script/`

```
cd ./script
```

2. Соберите образ со скриптом

```
docker-compose build
```

3. Запустите контейнер со скриптом

```
docker-compose run --rm script-cpu
```


## Папка `service`

В данной папке находится `docker-compose.yaml` для запуска бекенда для взаимодействия с API модели и фронтенда для визуализации работы с API.

Backend расположен по адресу `http://localhost:8910`, Swagger - `http://localhost:8910/docs`

Frontend расположен по адресу `http://localhost:8558`

Для запуска необходимо

1. Перейдите в папку `service/`

```
cd ./service
```

2. Соберите образ

```
docker-compose build
```

3. Запустите контейнеры

```
docker-compose up
```
