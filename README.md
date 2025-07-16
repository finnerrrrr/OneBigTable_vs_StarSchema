# Data Modeling Case Study

This mini-project explores two fundamentally different ways to model and store the same incoming workflow/recipe data:

1. **Normalized Relational Schema (3NF)**  
2. **One-Big-Table Array/JSONB Schema**

Below you will find the **reasoning**, **advantages & disadvantages**, and **ETL differences** for each approach.

---

## 1. Normalized Relational Schema (3NF)

### ERD

![Normalized ERD](docs/normalised_erd.png)

### 1.1. Reasoning
- **Decompose multi-valued attributes** (applications, categories, business objects) into their own tables.
- **Bridge tables** express many-to-many relationships explicitly.
- **Enforce referential integrity** via foreign keys.
- Ideal for OLTP workloads or any scenario requiring strict data consistency.

### 1.2. Advantages
- **Data integrity & consistency**  
  - Foreign keys guarantee that every `app_id`, `category_id`, `obj_id` actually exists.  
- **Fine-grained indexing & performance**  
  - B-Tree indexes on FK columns optimize joins and point-queries.  
- **Flexibility in queries**  
  - Easy to ask “which recipes use exactly these 4 apps?” via straightforward `JOIN … GROUP BY`.
- **Minimal data duplication**  
  - Shared lookup tables prevent repeating the same string in every row.

### 1.3. Disadvantages
- **Schema complexity**  
  - Many tables (5+), each with its own DDL and indexes.  
- **Join overhead**  
  - Complex queries require multiple joins, which can slow down analytics if data volumes grow.  
- **ETL complexity**  
  - Must explode lists, dedupe, build & load dimension tables, then bridge tables in the correct order.

### 1.4. ETL Process
1. **Read & Clean**  
   - Parse raw CSV, convert dates, strip & split multi-valued columns into Python lists.  
2. **Build Dimension DataFrames**  
   - `users_df`, `recipes_df`, `apps_df`, `cats_df`, `objs_df`.  
3. **Build Bridge DataFrames**  
   - `recipe_application_bridge`, `application_cat_bridge`, `application_obj_bridge`.  
4. **Load Sequence**  
   - Insert into dims first (`users`, `recipe`, `application`, `category`, `business_obj`).  
   - Then insert into bridge tables.  
5. **Error Handling & Idempotency**  
   - Use `INSERT … ON CONFLICT DO NOTHING` or upsert logic for safe re-runs.

---

## 2. One-Big-Table Array/JSONB Schema

![Normalized ERD](docs/onebigtable_erd.png)


### 2.1. Reasoning
- **Denormalize** applications, categories, and business objects directly into array or JSONB columns.
- **Single table** holds all recipe attributes, including multi-valued ones.
- Ideal for rapid prototyping, schemaless ingestion, or document-oriented workloads.

### 2.2. Advantages
- **Simplicity**  
  - Only one table (`recipes_array`), easy DDL and fewer moving parts.  
- **Fast writes**  
  - Insert one row per recipe—no need to manage multiple tables or bridge logic.  
- **Schema flexibility**  
  - JSONB column can adapt to new or evolving nested fields without DDL changes.  
- **Lower ETL overhead**  
  - No need to explode and dedupe lists into separate DataFrames.

### 2.3. Disadvantages
- **Weaker referential integrity**  
  - No FK constraints on array elements; the database cannot enforce that `AppX` exists.  
- **Query performance**  
  - Array/JSON containment queries (`@>`) are slower than B-Tree joins, even with GIN indexes.  
- **Duplication & storage**  
  - Repeated strings or JSON blobs in every row increase storage and cache pressure.  
- **Analytics limitations**  
  - Aggregations by individual elements require `UNNEST()`, which can be less efficient for large tables.

### 2.4. ETL Process
1. **Read & Clean**  
   - Parse CSV, convert dates, strip & split into Python lists (no need to explode).  
2. **Assemble Final DataFrame**  
   - Rename `id → recipe_id`, keep scalar columns, attach list-columns directly.  
3. **Load in One Step**  
   - Single call to `df.to_sql('recipes_array', …)` or `COPY` with array literals.  
4. **Indexing**  
   - Create GIN indexes on the array/JSONB columns to accelerate containment queries.

---

## 3. Side-by-Side ETL Comparison

| Step                        | Normalized Schema                      | One-Big-Table Schema          |
|-----------------------------|----------------------------------------|-------------------------------|
| **List handling**           | `.explode()` + dedupe                 | `.split()` → lists (no explode) |
| **Dimension load order**    | Load dims → load bridges               | N/A                           |
| **Number of loads**         | ≥ 8 separate table inserts             | 1 table insert               |
| **Integrity enforcement**   | DB-level FKs                           | Application-level checks only |
| **Loading complexity**      | High                                   | Low                           |
| **Need for upsert logic**   | Often yes                              | Rarely (overwrite or append)  |
| **Monitoring & retries**    | Per-table                            | Single operation              |

---

## 4. When to Choose Which

- **Choose Normalized** if you need:
  - Strong referential integrity and ACID compliance.
  - High query performance on complex joins.
  - Data models that rarely change and require rigorous governance.

- **Choose Array/JSONB** if you need:
  - Rapid ingestion of semi-structured or evolving payloads.
  - Minimal schema management for prototypes or small teams.
  - Simpler ETL pipelines with fewer moving parts.

---

## 5. Running the ETL

```bash
# 1) Set your environment:
export RAW_CSV=path/to/data/D_Data.csv
export DB_URL=postgresql://user:pass@host:5432/dbname

# 2) Normalized pipeline:
python etl/main_normalized.py

# 3) Array/JSONB pipeline:
python etl/main_array.py
