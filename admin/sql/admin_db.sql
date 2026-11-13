-- =====================================================================
-- admin_db : usuarios del panel, permisos por proyecto y auditoría
-- =====================================================================
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS users (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username         VARCHAR(64)  NOT NULL UNIQUE,
  email            VARCHAR(190) NULL,
  password_hash    VARCHAR(255) NOT NULL,
  role             ENUM('superadmin','editor') NOT NULL DEFAULT 'editor',
  is_active        TINYINT(1)   NOT NULL DEFAULT 1,
  failed_attempts  SMALLINT     NOT NULL DEFAULT 0,
  locked_until     DATETIME     NULL,
  last_login_at    DATETIME     NULL,
  created_at       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Qué proyectos puede tocar cada editor (superadmin los ve todos)
CREATE TABLE IF NOT EXISTS user_projects (
  user_id  INT UNSIGNED NOT NULL,
  project  VARCHAR(32)  NOT NULL,          -- winep3dia | trisat | st3lla
  PRIMARY KEY (user_id, project),
  CONSTRAINT fk_up_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS audit_log (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id     INT UNSIGNED NULL,
  username    VARCHAR(64)  NULL,
  project     VARCHAR(32)  NULL,
  entity      VARCHAR(64)  NULL,
  entity_id   VARCHAR(64)  NULL,
  action      VARCHAR(32)  NOT NULL,       -- login, login_failed, create, update, delete, publish
  details     JSON         NULL,
  ip          VARCHAR(45)  NULL,
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_audit_proj (project, created_at),
  KEY idx_audit_user (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
