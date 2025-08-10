-- 01_normalized_schema.sql
-- Drop everything first (in reverse-dependency order)
DROP TABLE IF EXISTS application_cat_bridge CASCADE;
DROP TABLE IF EXISTS application_obj_bridge CASCADE;
DROP TABLE IF EXISTS recipe_application_bridge CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS business_obj CASCADE;
DROP TABLE IF EXISTS application CASCADE;
DROP TABLE IF EXISTS recipe CASCADE;

-- ---------------------------------------------------
-- Recipe
-- ---------------------------------------------------
CREATE TABLE recipe (
  recipe_id            VARCHAR(255)     PRIMARY KEY,
  user_id              VARCHAR(255)     NOT NULL,
  version_no           INT              NOT NULL,
  name                 TEXT             NOT NULL,
  description          TEXT,
  created_at           TIMESTAMP        NOT NULL,
  updated_at           TIMESTAMP        NOT NULL,
  runnable             BOOLEAN          NOT NULL DEFAULT FALSE,
  running              BOOLEAN          NOT NULL DEFAULT FALSE,
  job_succeeded_count  INT              NOT NULL DEFAULT 0,
  job_failed_count     INT              NOT NULL DEFAULT 0,
  parent_id            VARCHAR(255),

  CONSTRAINT fk_recipe_parent
    FOREIGN KEY(parent_id) REFERENCES recipe(recipe_id)
);

-- ---------------------------------------------------
-- Application
-- ---------------------------------------------------
CREATE TABLE application (
  app_id   VARCHAR(255) PRIMARY KEY,
  name     TEXT          NOT NULL
);

-- ---------------------------------------------------
-- Business Object
-- ---------------------------------------------------
CREATE TABLE business_obj (
  obj_id   VARCHAR(255) PRIMARY KEY,
  name     TEXT          NOT NULL
);

-- ---------------------------------------------------
-- Category
-- ---------------------------------------------------
CREATE TABLE category (
  category_id VARCHAR(255) PRIMARY KEY,
  name        TEXT          NOT NULL
);

-- ---------------------------------------------------
-- Bridge: Recipe ↔ Application
-- ---------------------------------------------------
CREATE TABLE recipe_application_bridge (
  recipe_id VARCHAR(255) NOT NULL,
  app_id    VARCHAR(255) NOT NULL,
  PRIMARY KEY (recipe_id, app_id),

  CONSTRAINT fk_rab_recipe
    FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id),

  CONSTRAINT fk_rab_app
    FOREIGN KEY(app_id)    REFERENCES application(app_id)
);

-- ---------------------------------------------------
-- Bridge: Application ↔ Business Object
-- ---------------------------------------------------
CREATE TABLE application_obj_bridge (
  app_id VARCHAR(255) NOT NULL,
  obj_id VARCHAR(255) NOT NULL,
  PRIMARY KEY (app_id, obj_id),

  CONSTRAINT fk_aob_app
    FOREIGN KEY(app_id) REFERENCES application(app_id),

  CONSTRAINT fk_aob_obj
    FOREIGN KEY(obj_id)  REFERENCES business_obj(obj_id)
);

-- ---------------------------------------------------
-- Bridge: Application ↔ Category
-- ---------------------------------------------------
CREATE TABLE application_cat_bridge (
  app_id      VARCHAR(255) NOT NULL,
  category_id VARCHAR(255) NOT NULL,
  PRIMARY KEY (app_id, category_id),

  CONSTRAINT fk_acb_app
    FOREIGN KEY(app_id)      REFERENCES application(app_id),

  CONSTRAINT fk_acb_category
    FOREIGN KEY(category_id) REFERENCES category(category_id)
);
