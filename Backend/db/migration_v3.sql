CREATE TABLE IF NOT EXISTS audit_logs (
  audit_id      UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  supervisor_id VARCHAR(36)  NOT NULL REFERENCES users(user_id),
  action        VARCHAR(50)  NOT NULL,
  target_type   VARCHAR(10)  NOT NULL,
  target_id     VARCHAR(36)  NOT NULL,
  target_name   VARCHAR(255) NOT NULL,
  timestamp     TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_supervisor ON audit_logs(supervisor_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp  ON audit_logs(timestamp DESC);
