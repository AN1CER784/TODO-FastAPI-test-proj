# TODO-FastAPI-test-proj

Тестовый проект на FastAPI для управления задачами (TODO), с настройками для контейнеризации и миграций. Репозиторий содержит исходники приложения, Dockerfile и docker-compose (см. файлы в репозитории). ([GitHub][1])


## 1. Основной функционал API

(Ожидаемая базовая функциональность, типовая для TODO-приложения — проверьте реальные роуты в `src/`):

* Создание задачи (POST `/tasks`)
* Получение списка задач (GET `/tasks`)
* Получение одной задачи (GET `/tasks/{id}`)
* Обновление задачи (PUT `/tasks/{id}`)
* Удаление задачи (DELETE `/tasks/{id}`)
* (Опционально) фильтрация / пагинация / пометка статуса (done/undone)

---

## 2. Быстрый старт — запуск через Docker / Docker Compose

### Команды

1. Склонируйте репозиторий:

```bash
git clone https://github.com/AN1CER784/TODO-FastAPI-test-proj.git
cd TODO-FastAPI-test-proj
```

2. Запустите через docker-compose:

```bash
docker-compose up --build
```

3. Откройте в браузере:

* Документация Swagger: `http://localhost:8000/docs`
* Redoc: `http://localhost:8000/redoc`

---

## 3. Тесты

Запуск тестов через docker-compose ():

```bash
docker container exec -it fastapitodo-web-1 pytest
```

