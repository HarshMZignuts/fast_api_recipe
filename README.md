# 🍲 FastAPI Recipe Project

This project is built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, with support for authentication, password hashing, and database migrations.

---

## 🚀 Setup Instructions

### 1. Create Virtual Environment

```bash
python3 -m venv recipe_venv
```

### 2. Activate Virtual Environment

```bash
source recipe_venv/bin/activate
```

---

## 📦 Install Dependencies

### FastAPI

```bash
pip install fastapi
```

### Uvicorn (ASGI Server)

```bash
pip install "uvicorn[standard]"
```

### SQLAlchemy (Database ORM)

```bash
pip install sqlalchemy
```

### Pydantic (Data Validation & Models)

> Used for request/response schema validation

---

## 🔐 Authentication & Security

### Password Hashing

```bash
pip install passlib
pip install bcrypt==4.0.1
```

> ⚠️ Important: Use a compatible `bcrypt` version with `passlib`

### JWT Authentication

```bash
pip install "python-jose[cryptography]"
```

### Generate Secret Key

```bash
openssl rand -hex 32
```

---

## 📁 File Upload Support (Optional)

```bash
pip install python-multipart
```

> Used for handling `multipart/form-data` (currently not used in this project)

---

## 🗄️ Database Setup (PostgreSQL)

### PostgreSQL Driver

```bash
pip install psycopg2-binary
```

---

## 🔄 Database Migration (Alembic)

### Install Alembic

```bash
pip install alembic
```

### Initialize Alembic

```bash
alembic init <folder_name>
```

### Create Migration Revision

```bash
alembic revision -m "your message"
```

### Apply Migration (Upgrade DB)

```bash
alembic upgrade <revision_id>
```

---

## 🧠 Tech Stack Summary

* **FastAPI** → API framework
* **Uvicorn** → ASGI server
* **SQLAlchemy** → ORM for database operations
* **Pydantic** → Data validation
* **PostgreSQL** → Database
* **Alembic** → Migration tool
* **Passlib + Bcrypt** → Password hashing
* **Python-JOSE** → JWT authentication

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

---

## 📌 Notes

* Ensure virtual environment is activated before running commands
* Keep your secret key secure
* Always run migrations after schema changes

