-- =====================================================================
-- winep3dia_db : enciclopedia WINEp3dIA (artículos, fichas, fuentes)
-- MariaDB 10.6 · utf8mb4
-- =====================================================================
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS standards (
  code        VARCHAR(16)  NOT NULL PRIMARY KEY,          -- WSET3 | CMS | ASI
  name_es     VARCHAR(120) NOT NULL,
  name_en     VARCHAR(120) NOT NULL,
  color       VARCHAR(24)  NOT NULL DEFAULT 'slate',
  sort_order  SMALLINT     NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS categories (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  slug        VARCHAR(120) NOT NULL UNIQUE,
  name_es     VARCHAR(200) NOT NULL,
  name_en     VARCHAR(200) NULL,
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS articles (
  id                INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  slug              VARCHAR(160) NOT NULL UNIQUE,
  standard_code     VARCHAR(16)  NOT NULL,
  category_id       INT UNSIGNED NULL,
  badge_color       VARCHAR(24)  NOT NULL DEFAULT 'slate',
  title_es          VARCHAR(255) NOT NULL,
  title_en          VARCHAR(255) NULL,
  summary_es        TEXT         NULL,
  summary_en        TEXT         NULL,
  content_es        MEDIUMTEXT   NULL,
  content_en        MEDIUMTEXT   NULL,
  key_takeaways_es  JSON         NULL,
  key_takeaways_en  JSON         NULL,
  related_grapes    JSON         NULL,
  related_regions   JSON         NULL,
  tags              JSON         NULL,
  status            ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  updated_by        VARCHAR(64)  NULL,
  CONSTRAINT fk_art_std FOREIGN KEY (standard_code) REFERENCES standards(code) ON UPDATE CASCADE,
  CONSTRAINT fk_art_cat FOREIGN KEY (category_id)   REFERENCES categories(id) ON DELETE SET NULL,
  KEY idx_art_status_std (status, standard_code),
  FULLTEXT KEY ft_art_es (title_es, summary_es, content_es),
  FULLTEXT KEY ft_art_en (title_en, summary_en, content_en)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS cards (
  id             INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  slug           VARCHAR(160) NOT NULL UNIQUE,
  standard_code  VARCHAR(16)  NOT NULL,
  category_id    INT UNSIGNED NULL,
  question_es    TEXT         NOT NULL,
  question_en    TEXT         NULL,
  answer_es      TEXT         NOT NULL,
  answer_en      TEXT         NULL,
  solution_es    TEXT         NULL,
  solution_en    TEXT         NULL,
  citation       VARCHAR(500) NULL,
  difficulty     TINYINT UNSIGNED NOT NULL DEFAULT 2,     -- 1 básico · 2 medio · 3 avanzado
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  updated_by     VARCHAR(64)  NULL,
  CONSTRAINT fk_card_std FOREIGN KEY (standard_code) REFERENCES standards(code) ON UPDATE CASCADE,
  CONSTRAINT fk_card_cat FOREIGN KEY (category_id)   REFERENCES categories(id) ON DELETE SET NULL,
  KEY idx_card_status_std (status, standard_code),
  FULLTEXT KEY ft_card_es (question_es, answer_es, solution_es)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bibliografía / fuentes ("references" es palabra reservada en SQL)
CREATE TABLE IF NOT EXISTS sources (
  id           INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  slug         VARCHAR(120) NOT NULL UNIQUE,
  title        VARCHAR(300) NOT NULL,
  authors      VARCHAR(300) NULL,
  publisher    VARCHAR(300) NULL,
  year         SMALLINT     NULL,
  kind         ENUM('book','database','organization','website','article') NOT NULL DEFAULT 'book',
  url          VARCHAR(500) NULL,
  label_es     VARCHAR(120) NULL,
  label_en     VARCHAR(120) NULL,
  note_es      TEXT         NULL,
  note_en      TEXT         NULL,
  sort_order   SMALLINT     NOT NULL DEFAULT 0,
  status       ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  updated_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS article_sources (
  article_id  INT UNSIGNED NOT NULL,
  source_id   INT UNSIGNED NOT NULL,
  PRIMARY KEY (article_id, source_id),
  CONSTRAINT fk_as_art FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
  CONSTRAINT fk_as_src FOREIGN KEY (source_id)  REFERENCES sources(id)  ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO standards (code, name_es, name_en, color, sort_order) VALUES
 ('WSET3','WSET Nivel 3','WSET Level 3','amber',1),
 ('CMS','Court of Master Sommeliers (Deductivo)','Court of Master Sommeliers (Deductive)','rose',2),
 ('ASI','ASI Global','ASI Global','emerald',3);
