-- DROP existing (if you’re iterating)
DROP TABLE IF EXISTS recipes_array;

-- Single‐table “array/JSONB” model
CREATE TABLE recipes_array (
  recipe_id            TEXT            PRIMARY KEY,
  user_id              TEXT            NOT NULL,
  version_no           INT             NOT NULL,
  name                 TEXT            NOT NULL,
  description          TEXT,
  created_at           TIMESTAMP       NOT NULL,
  updated_at           TIMESTAMP       NOT NULL,
  runnable             BOOLEAN         NOT NULL DEFAULT FALSE,
  running              BOOLEAN         NOT NULL DEFAULT FALSE,
  job_succeeded_count  INT             NOT NULL DEFAULT 0,
  job_failed_count     INT             NOT NULL DEFAULT 0,
  parent_id            TEXT,

  -- multi‐valued attributes as arrays
  applications         TEXT[]          NOT NULL DEFAULT ARRAY[]::TEXT[],
  categories           TEXT[]          NOT NULL DEFAULT ARRAY[]::TEXT[],
  business_objects     TEXT[]          NOT NULL DEFAULT ARRAY[]::TEXT[],
);

-- GIN indexes to speed up searching for array columns
CREATE INDEX idx_recipes_array_apps_gin
  ON recipes_array USING GIN (applications);

CREATE INDEX idx_recipes_array_cats_gin
  ON recipes_array USING GIN (categories);

CREATE INDEX idx_recipes_array_objs_gin
  ON recipes_array USING GIN (business_objects);