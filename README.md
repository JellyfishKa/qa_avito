# Тестовое задание QA-стажировка Avito

Здесь лежат оба задания.

---

## Задание 1 — баги на скриншоте

Нашёл 8 багов, расписал в [BUGS_SCREENSHOT.md](BUGS_SCREENSHOT.md)

## Задание 2.1 — API

Тест-кейсы: [TESTCASES.md](TESTCASES.md)  
Баги, найденные при прогоне: [BUGS.md](BUGS.md)

Сервис: `https://qa-internship.avito.com`

### Как запустить тесты

```bash
git clone <ссылка на репо>
cd qa_avito

pip install -r requirements.txt

pytest tests/ -v
```

Тесты гоняются против живого API, поэтому нужен интернет. Часть тестов намеренно падает — это баги сервиса, описаны в BUGS.md.

### Структура проекта

```
tests/
    conftest.py          — фикстуры (клиент, созданное объявление)
    test_create_item.py  — тесты создания
    test_get_item.py     — тесты получения по id
    test_get_seller.py   — тесты получения по продавцу
    test_statistic.py    — тесты статистики
    test_e2e.py          — сквозные сценарии
helpers/
    api_client.py        — обёртка над requests
    data_generator.py    — генерация данных для тестов
```

### Линтер и форматтер

```bash
flake8 tests/ helpers/
black tests/ helpers/
```
