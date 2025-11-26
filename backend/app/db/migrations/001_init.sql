-- БД1: Клиенты
-- Также добавили минимальные ограничения для целостности.

CREATE TABLE IF NOT EXISTS clients (
  id BIGSERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  date_of_birth DATE NOT NULL,

  passport_series VARCHAR(4) NOT NULL,
  passport_number VARCHAR(6) NOT NULL,

  address_registration TEXT NOT NULL,
  phone VARCHAR(32) NOT NULL,
  email VARCHAR(255) NOT NULL,

  workplace TEXT NOT NULL,
  position TEXT NOT NULL,
  monthly_income NUMERIC(12,2) NOT NULL CHECK (monthly_income > 0),

  registered_at TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT uq_client_passport UNIQUE (passport_series, passport_number)
);

-- БД2: Кредитные заявки
CREATE TABLE IF NOT EXISTS credit_applications (
  id BIGSERIAL PRIMARY KEY,
  client_id BIGINT NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,

  submitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  requested_amount NUMERIC(12,2) NOT NULL CHECK (requested_amount > 0),
  term_months INT NOT NULL CHECK (term_months > 0),
  purpose TEXT NOT NULL,

  status VARCHAR(16) NOT NULL DEFAULT 'NEW',
  status_changed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  interest_rate NUMERIC(5,2),
  comment TEXT,

  CONSTRAINT ck_credit_status CHECK (status IN ('NEW', 'APPROVED', 'REJECTED'))
);

CREATE INDEX IF NOT EXISTS idx_credit_apps_client_id ON credit_applications(client_id);
