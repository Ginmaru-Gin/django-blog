# STUDY-DJANGO-BLOG
# Описание
Простой блог, созданный в процессе изучения django.

## Инструкции по процессу разработки

### Стиль коммитов
[Соглашение по коммитам](https://www.conventionalcommits.org/en/v1.0.0/)

### Linux

#### Требуемые пакеты
- python3
- python3-venv
- postgresql
- libpq-dev

```bash
sudo apt install python3 python3-venv postgresql libpq-dev
```

#### Развёртывание
Настройка БД
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE blog;
CREATE USER blog_admin WITH PASSWORD 'admin';
ALTER ROLE blog_admin SET client_encoding TO 'utf8';
ALTER ROLE blog_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE blog_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE blog TO blog_admin;
\q
```
Настройка django-проекта
```bash
git clone git@github.com:Ginmaru-Gin/study-django-blog.git
cd study-django-blog/django-blog
git checkout dev
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```
Создание администратора
```bash
python3 manage.py createsuperuser
```
Запуск сервера
```bash
python3 manage.py runserver
```
