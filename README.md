# СОК (MVP) — Система обработки кредитных заявок

Учебный MVP проекта “СОК”: клиент может создать карточку клиента и подать кредитную заявку, система выдаёт решение (упрощённое). Сотрудник может войти, просматривать списки, фильтровать заявки, менять статус (одобрить/отклонить). Для администратора доступен просмотр аудита.

## Стек

**Backend**
- Python + FastAPI
- PostgreSQL
- psycopg2 (подключение к БД)
- JWT (Bearer token)
- Хэширование паролей: PBKDF2 (stdlib, без bcrypt)

**Frontend**
- Vue 3 + Vite
- Vue Router
- (для demo) Nginx как reverse proxy: `/api` проксируется в backend

---

## Реализованная функциональность

### Публичная часть (клиент)
- Создание клиента (карточка клиента)
- Получение клиента по ID
- Подача кредитной заявки
- Получение заявки по ID
- Авто-решение по заявке (упрощённый скоринг для MVP)

### Сотрудник (JWT)
- Логин сотрудника (OAuth2 password flow) → получение JWT
- Просмотр списков:
  - список клиентов (только сотрудник/админ)
  - список заявок (только сотрудник/админ)
- Фильтр заявок по статусу: `ALL / NEW / APPROVED / REJECTED`
- Изменение статуса заявки (approve/reject) через `PATCH` (только сотрудник/админ)

### Админ
- Просмотр аудита (последние N событий) — только `ADMIN`
- В WebUI отображается кнопка **“Показать аудит”** только для `ADMIN`

### Аудит (security log)
Логируем ключевые действия (без “сырых” персональных данных):
- `CLIENT_CREATE`, `CLIENT_READ`, `CLIENT_LIST`
- `APPLICATION_CREATE`, `APPLICATION_READ`, `APPLICATION_LIST`, `APPLICATION_UPDATE`

`meta` в аудите содержит только безопасные поля (например: `limit/offset/status`, либо параметры заявки), **без паспорта/телефона/email**.

---

## Запуск (самый простой вариант — demo через Docker)

### 1) Запуск всего проекта одной командой
В корне проекта:
```bash
docker compose -f docker-compose.demo.yml up --build
```

Открыть:
- WebUI: http://localhost:8080
- Swagger API: http://localhost:8000/docs

> В demo-режиме фронт общается с бэком через Nginx: `/api -> backend:8000/api`, поэтому CORS обычно не мешает.

### 2) Полная пересборка “с нуля” (если нужно)
ОСТОРОЖНО: удаляет данные Postgres (volume).
```bash
docker compose -f docker-compose.demo.yml down --volumes --remove-orphans --rmi local
docker compose -f docker-compose.demo.yml build --no-cache
docker compose -f docker-compose.demo.yml up --force-recreate
```

---

## Локальная разработка (без demo Nginx)

### Требования
- Python (желательно 3.11+)
- Node.js (16+)
- Docker (для Postgres)

### 1) База данных
Если у вас есть docker-compose для БД:
```bash
docker compose up -d
```

Если нет — используйте demo и просто поднимите db (или поднимайте всё целиком):
```bash
docker compose -f docker-compose.demo.yml up -d db
```

### 2) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate

cp .env.example .env
pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger:
- http://localhost:8000/docs

### 3) Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Открыть:
- http://localhost:5173

---

## Учётные данные (по умолчанию)

При старте backend делается `seed_admin()`:
- `ADMIN_USERNAME=admin`
- `ADMIN_PASSWORD=admin123`

Если вы поменяли пароль/алгоритм хэширования — при запуске seed обновит пароль админа по `.env`.

---

## WebUI сценарии (что показать на защите)

### Клиент
1) Вкладка **Клиент** → создать клиента  
2) Вкладка **Заявка** → подать заявку (получить статус APPROVED/REJECTED)  
3) Вкладка **Статус** → проверить заявку по ID  

### Сотрудник
1) **Сотрудник** → `/employee/login` → войти `admin/admin123`  
2) **Кабинет сотрудника** → список клиентов и заявок  
3) Поставить фильтр по статусу  
4) Нажать **Одобрить/Отклонить** у заявки → статус меняется  
5) (Опционально) Нажать **Показать аудит** (если `ADMIN`) → увидеть события

---

## API (кратко)

### Public
- `POST /api/clients`
- `GET /api/clients/{id}`
- `POST /api/applications`
- `GET /api/applications/{id}`

### Auth
- `POST /api/auth/token` (form-urlencoded: `username`, `password`)
- `GET /api/auth/me`

### Employee/Admin only (Bearer JWT)
- `GET /api/clients?limit=&offset=`
- `GET /api/applications?limit=&offset=&status=APPROVED|REJECTED|NEW`
- `PATCH /api/applications/{id}` (например: `{ "status": "APPROVED" }`)

### Admin only
- `GET /api/audit?limit=50`

---

## Переменные окружения (важные)

Backend (`backend/.env`):
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `CORS_ORIGINS` (например: `http://localhost:5173`)
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRES_MINUTES`
- `ADMIN_USERNAME`, `ADMIN_PASSWORD`
- `LOG_LEVEL`

Frontend (`frontend/.env`):
- `VITE_API_BASE_URL` (например: `http://localhost:8000/api` или `/api` для demo)

---

## Структура проекта (упрощённо)

Backend:
- `app/api/*` — роуты (контроллеры)
- `app/*/service.py` — логика (сервисы)
- `app/*/repository.py` — работа с БД
- `app/db/*` — init_db и миграции
- `app/auth/*` — JWT/auth/seed
- `app/audit/*` — аудит

Frontend:
- `src/pages/*` — страницы (CreateClient, CreateApplication, Status, Employee*)
- `src/api.js` — запросы к API
- `src/auth.js` — хранение токена
- `src/router.js` — маршрутизация

---

## Частые проблемы

- **WARN про POSTGRES_* переменные при `docker compose build`**  
  Это значит, что в compose-файле используются переменные `${POSTGRES_DB}` и т.п., но у вас не задан `.env` рядом с compose. Решение: задать переменные в `.env` или прописать их прямо в compose.

- **`Form data requires python-multipart`**  
  Нужен пакет `python-multipart`, потому что `/auth/token` принимает form-urlencoded.

- **“не отображается аудит”**  
  Проверьте, что вошли под ролью `ADMIN`. Кнопка “Показать аудит” скрыта для не-ADMIN.

---

## Лицензия
Учебный проект / MVP для лабораторной работы.
