<div align="center">

# ✅ TodoApp API

**A REST API for task management with JWT authentication and role-based access control.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

</div>

---

## 📖 About the project

**TodoApp** is an API built with **FastAPI** to manage to-do lists securely. Each user signs up, logs in, and can access only **their own tasks**. Users with the **admin** role have exclusive routes to oversee all tasks in the system.

The project is organized in layers (models, database, routers) and uses **Alembic** to version database changes.

## ✨ Features

- 🔐 **JWT authentication** (login via OAuth2 Password Flow, token valid for 20 minutes)
- 🔑 **Protected passwords** hashed with bcrypt
- 📝 **Full task CRUD** (create, list, retrieve, update, and delete)
- 👤 **Data isolation:** each user sees only their own tasks
- 🛡️ **Admin routes** protected by role (`role`)
- 🔄 **Password change** with current password verification
- ✔️ **Data validation** with Pydantic (field lengths, priority from 1 to 5, etc.)
- 🗃️ **Database migrations** with Alembic
- 📚 **Automatic interactive documentation** (Swagger UI and ReDoc)

## 🛠️ Tech stack

| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM |
| [SQLite](https://www.sqlite.org/) | Database |
| [Alembic](https://alembic.sqlalchemy.org/) | Migrations |
| [Pydantic](https://docs.pydantic.dev/) | Data validation |
| [python-jose](https://github.com/mpdavis/python-jose) | JWT generation and validation |
| [Passlib (bcrypt)](https://passlib.readthedocs.io/) | Password hashing |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |

## 📁 Project structure

```
TodoApp/
├── alembic/
│   └── versions/
│       └── a03c45be11b6_create_phone_number_column_for_users_table.py
├── routers/
│   ├── admin.py      # Admin-only routes
│   ├── auth.py       # Sign-up, login, and token generation
│   ├── todos.py      # Task CRUD
│   └── users.py      # Profile and password change
├── database.py       # Database connection and session
├── models.py         # Users and Todos models
└── main.py           # Application entry point
```

## 🗄️ Data model

**Users**

| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `email` | String | Unique |
| `username` | String | Unique |
| `first_name` | String | |
| `last_name` | String | |
| `hashed_password` | String | bcrypt-hashed password |
| `is_active` | Boolean | Default: `True` |
| `role` | String | E.g. `admin`, `user` |
| `phone_number` | String | Added via migration |

**Todos**

| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | String | |
| `description` | String | |
| `priority` | Integer | From 1 to 5 |
| `complete` | Boolean | Default: `False` |
| `owner_id` | Integer | FK to `users.id` |

## 🚀 Getting started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/your-repository.git
cd your-repository/TodoApp

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install fastapi uvicorn sqlalchemy alembic "passlib[bcrypt]" "python-jose[cryptography]" python-multipart

# 4. (Optional) Apply migrations
alembic upgrade head

# 5. Start the server
uvicorn main:app --reload
```

> 💡 Tables are also created automatically on first run (`models.Base.metadata.create_all`).

> ⚠️ If you get a bcrypt-related error with passlib, install a compatible version: `pip install bcrypt==4.0.1`

The API will be available at **http://127.0.0.1:8000**

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

## 🔌 Endpoints

### 🔐 Authentication — `/auth`

| Method | Route | Description | Auth |
|---|---|---|:---:|
| `POST` | `/auth/` | Registers a new user | ❌ |
| `POST` | `/auth/token` | Logs in and returns the JWT | ❌ |

### 📝 Todos

| Method | Route | Description | Auth |
|---|---|---|:---:|
| `GET` | `/todo` | Lists the logged-in user's tasks | ✅ |
| `GET` | `/todo/{todo_id}` | Retrieves a task by ID | ✅ |
| `POST` | `/todo` | Creates a new task | ✅ |
| `PUT` | `/todo/{todo_id}` | Updates a task | ✅ |
| `DELETE` | `/todo/{todo_id}` | Deletes a task | ✅ |

### 👤 Users — `/users`

| Method | Route | Description | Auth |
|---|---|---|:---:|
| `GET` | `/users/users` | Returns the logged-in user's data | ✅ |
| `PUT` | `/users/users` | Changes the logged-in user's password | ✅ |

### 🛡️ Admin — `/admin`

| Method | Route | Description | Auth |
|---|---|---|:---:|
| `GET` | `/admin/todo` | Lists tasks from **all** users | 🔒 admin |
| `DELETE` | `/admin/todo/{todo_id}` | Deletes a task | 🔒 admin |

## 💡 Usage examples

**1. Create a user**

```bash
curl -X POST http://127.0.0.1:8000/auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maria@email.com",
    "username": "maria",
    "first_name": "Maria",
    "last_name": "Silva",
    "password": "123456",
    "role": "admin"
  }'
```

**2. Log in and get the token**

```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -d "username=maria&password=123456"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**3. Create a task**

```bash
curl -X POST http://127.0.0.1:8000/todo \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Study FastAPI",
    "description": "Finish the todo list project",
    "priority": 5,
    "complete": false
  }'
```

**4. List your tasks**

```bash
curl http://127.0.0.1:8000/todo \
  -H "Authorization: Bearer YOUR_TOKEN"
```

> 🧪 **Tip:** in Swagger UI (`/docs`), click **Authorize** and enter your username and password to test all protected routes right in the browser.

## ✅ Validation rules

- **User:** `email`, `username`, `first_name`, and `last_name` must have at least 3 characters; `password` must have at least 6
- **Todo:** `title` must have at least 3 characters; `description` must be between 3 and 100 characters; `priority` must be between 1 and 5

## 🔄 Migrations with Alembic

```bash
# Apply all migrations
alembic upgrade head

# Revert the last migration
alembic downgrade -1

# Create a new migration
alembic revision -m "description of the change"
```

## 🗺️ Roadmap

- [ ] Move `SECRET_KEY` to environment variables (`.env`)
- [ ] Allow `phone_number` during sign-up
- [ ] Add automated tests with `pytest`
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Dockerize the application

## 🤝 Contributing

Contributions are welcome! Feel free to open an *issue* or submit a *pull request*.

1. Fork the project
2. Create a branch: `git checkout -b my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin my-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with 💙 and FastAPI by **[Your Name](https://github.com/your-username)**

</div>
