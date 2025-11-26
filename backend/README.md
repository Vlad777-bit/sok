## СОК (MVP) — Backend

### 1) Запустить Postgres

```sh
cp .env.example .env
docker compose up -d
```

### 2) Backend

```sh
cd backend
python -m venv .venv
```

# Windows: .venv\Scripts\activate

```sh
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3) Проверка

GET http://localhost:8000/api/ping

GET http://localhost:8000/api/health
