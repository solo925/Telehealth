Here’s an overview of PostgreSQL (often referred to as Postgres) database commands and key concepts, categorized for ease of reference:

### 1. **Connection Commands**

- **Connect to a database:**
  ```bash
  psql -h host -U username -d database
  ```
- **Connect as superuser (default postgres user):**

  ```bash
  sudo -u postgres psql
  ```

- **Switch between databases:**
  ```sql
  \c database_name;
  ```

### 2. **Database Management**

- **Create a database:**
  ```sql
  CREATE DATABASE database_name;
  ```
- **Drop a database:**
  ```sql
  DROP DATABASE IF EXISTS database_name;
  ```
- **List all databases:**
  ```sql
  \l
  ```

### 3. **User Management**

- **Create a user:**
  ```sql
  CREATE USER username WITH PASSWORD 'password';
  ```
- **Alter a user’s password:**
  ```sql
  ALTER USER username WITH PASSWORD 'new_password';
  ```
- **Grant privileges to a user:**
  ```sql
  GRANT ALL PRIVILEGES ON DATABASE database_name TO username;
  ```
- **Revoke privileges:**
  ```sql
  REVOKE ALL PRIVILEGES ON DATABASE database_name FROM username;
  ```
- **List users:**
  ```sql
  \du
  ```

### 4. **Table Management**

- **Create a table:**
  ```sql
  CREATE TABLE table_name (
    id SERIAL PRIMARY KEY,
    column_name data_type,
    another_column data_type
  );
  ```
- **Drop a table:**
  ```sql
  DROP TABLE IF EXISTS table_name;
  ```
- **Rename a table:**
  ```sql
  ALTER TABLE old_table_name RENAME TO new_table_name;
  ```
- **List all tables in a database:**
  ```sql
  \dt
  ```

### 5. **Schema Management**

- **Create a schema:**
  ```sql
  CREATE SCHEMA schema_name;
  ```
- **Drop a schema:**
  ```sql
  DROP SCHEMA schema_name CASCADE;
  ```
- **Set default schema for session:**
  ```sql
  SET search_path TO schema_name;
  ```

### 6. **Inserting, Updating, and Deleting Data**

- **Insert data into a table:**
  ```sql
  INSERT INTO table_name (column1, column2) VALUES (value1, value2);
  ```
- **Update data in a table:**
  ```sql
  UPDATE table_name SET column1 = value1 WHERE condition;
  ```
- **Delete data from a table:**
  ```sql
  DELETE FROM table_name WHERE condition;
  ```

### 7. **Querying Data**

- **Select all records:**
  ```sql
  SELECT * FROM table_name;
  ```
- **Select specific columns:**
  ```sql
  SELECT column1, column2 FROM table_name;
  ```
- **Filter results with `WHERE`:**
  ```sql
  SELECT * FROM table_name WHERE column1 = value1;
  ```
- **Join two tables:**
  ```sql
  SELECT * FROM table1 JOIN table2 ON table1.column = table2.column;
  ```

### 8. **Indexes**

- **Create an index:**
  ```sql
  CREATE INDEX index_name ON table_name (column_name);
  ```
- **Drop an index:**
  ```sql
  DROP INDEX IF EXISTS index_name;
  ```

### 9. **Transactions**

- **Begin a transaction:**
  ```sql
  BEGIN;
  ```
- **Commit a transaction:**
  ```sql
  COMMIT;
  ```
- **Rollback a transaction:**
  ```sql
  ROLLBACK;
  ```

### 10. **Views**

- **Create a view:**
  ```sql
  CREATE VIEW view_name AS SELECT column1, column2 FROM table_name WHERE condition;
  ```
- **Drop a view:**
  ```sql
  DROP VIEW IF EXISTS view_name;
  ```

### 11. **Backup and Restore**

- **Backup a database:**
  ```bash
  pg_dump -U username -d database_name -f backup.sql
  ```
- **Restore a database:**
  ```bash
  psql -U username -d database_name -f backup.sql
  ```

### 12. **Miscellaneous**

- **Get PostgreSQL version:**
  ```sql
  SELECT version();
  ```
- **Describe a table’s structure:**
  ```sql
  \d table_name
  ```
- **Exit `psql`:**
  ```bash
  \q
  ```

### 13. **PostgreSQL Configuration**

- **Show all server configuration parameters:**
  ```sql
  SHOW ALL;
  ```
- **Set a configuration parameter:**
  ```sql
  SET parameter_name TO value;
  ```

These commands are the basics of working with PostgreSQL databases, allowing you to create and manage databases, users, tables, and data, and perform other administrative tasks.
