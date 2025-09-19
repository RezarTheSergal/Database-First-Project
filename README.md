Десктопное-приложение для взаимодействия с БД

## Участники
- Валекжанин Владимир - Frontend Developer
- Амвросов Максим - Frontend Developer
- Шаломеенко Анастасия - QA Engineer
- Ляпунов Даниил - Data Scientist
- Кочегаров Михаил - Backend Developer

## Стек
- Язык: Python
- GUI: PySide6
- БД: PostgreSQL + SQLAlchemy
- Юнит-тестирование: pytest

## Локальный запуск

В корне проекта:

```bash
python -m venv venv

source venv/Scripts/activate # Windows
# ИЛИ
source venv/bin/activate # Linux

pip install -r requirements.txt
```

## Работа с БД

Для упрощённой работы с БД используется библиотека [alembic](https://rutube.ru/video/fa453d4fa9b31e028cc4db5786d091b8/?r=wd&p=EAFBAIUOor1oyyQIlfX1Qw)

Используется в качестве упрощения контроля версий БД, позволяет автоматически генерировать и применять [скрипты миграций](https://www.google.com/search?q=%D1%87%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D1%8B+%D0%BC%D0%B8%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D0%B9+alembic&sca_esv=9dbcedb0407ac63c&rlz=1C1CHBD_enRU1029RU1029&ei=lmnEaMDrIo_awPAPlvKpuQk&ved=0ahUKEwjAjpeh8NOPAxUPLRAIHRZ5KpcQ4dUDCBA&uact=5&oq=%D1%87%D1%82%D0%BE+%D1%82%D0%B0%D0%BA%D0%BE%D0%B5+%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D1%8B+%D0%BC%D0%B8%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D0%B9+alembic&gs_lp=Egxnd3Mtd2l6LXNlcnAiOdGH0YLQviDRgtCw0LrQvtC1INGB0LrRgNC40L_RgtGLINC80LjQs9GA0LDRhtC40LkgYWxlbWJpYzIFECEYoAFIpj5QAFjeOnAAeAGQAQCYAWCgAcIRqgECMzS4AQPIAQD4AQGYAiKgApoSwgIOEC4YgAQYsQMYgwEYigXCAgsQABiABBixAxiDAcICCBAAGIAEGLEDwgIFEAAYgATCAgQQABgDwgIIEC4YgAQYsQPCAh0QLhiABBixAxiDARiKBRiXBRjcBBjeBBjfBNgBAcICChAAGIAEGEMYigXCAg4QABiABBixAxiDARiKBcICCxAAGIAEGLEDGMkDwgILEAAYgAQYkgMYigXCAgYQABgWGB7CAggQABiABBiiBMICBBAhGBXCAgUQIRifBcICCBAAGAgYDRgewgIHECEYoAEYCsICCRAhGKABGAoYKpgDALoGBggBEAEYFJIHAjM0oAfn0QGyBwIzNLgHmhLCBwY2LjI1LjPIB0c&sclient=gws-wiz-serp).

Основные комманды (для разработчика БД):
- ```alembic init --template generic alembic``` - внедрение синхронной системы миграций в проект
- ```python -m alembic revision --autogenerate -m "[Some useful migration info]"``` - сгенерировать миграцию
- ```python -m alembic upgrade head``` - применить миграции

## Пометки к ветке

БД создана в целях настройки alembic и sqlalchemy, а так же ради примера :D
