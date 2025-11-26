-- Журналирование действий.
-- Важно: не храним паспорт/телефон/email целиком в audit_log, только факт действий и идентификаторы.

CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

  actor_user_id BIGINT,
  actor_username VARCHAR(64),
  actor_role VARCHAR(16),

  action VARCHAR(64) NOT NULL,
  entity VARCHAR(64) NOT NULL,
  entity_id BIGINT,

  meta JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_actor_user_id ON audit_logs(actor_user_id);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_logs(entity, entity_id);
