# ✅ Todo Management System

A full-stack Todo Management System built with **Python, FastAPI, Streamlit, PostgreSQL, and Docker**. The application allows users to create, view, edit, complete, and delete tasks through a web interface.

## 🚀 Features

- **Create Tasks:** Add a task with a title and description.
- **View Tasks:** Display all saved tasks.
- **Edit Tasks:** Update task titles and descriptions.
- **Task Status:** Mark tasks as completed or pending.
- **Delete Tasks:** Remove tasks with a confirmation step.
- **REST API:** Manage tasks through FastAPI endpoints.
- **Data Persistence:** Store tasks in PostgreSQL.
- **Containerized Database:** Run PostgreSQL using Docker Compose.
- **API Documentation:** Explore and test endpoints using Swagger UI.
- **Automated Testing:** Test application behavior using pytest.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API development |
| Streamlit | Web user interface |
| PostgreSQL | Relational database |
| Psycopg | Python–PostgreSQL connectivity |
| Docker | Database containerization |
| Docker Compose | Database service configuration |
| Pytest | Automated testing |
| Git and GitHub | Version control and project hosting |

## 🏗️ Architecture

```text
                 User
                  |
                  v
          +----------------+
          |   Streamlit    |
          |   Frontend     |
          +----------------+
                  |
                  | HTTP Requests
                  v
          +----------------+
          |    FastAPI     |
          |   REST API     |
          +----------------+
                  |
                  | SQL Queries
                  v
          +----------------+
          |  PostgreSQL    |
          |    Database    |
          +----------------+
                  |
                  v
             Docker
```

## 📁 Project Structure

```text
Project-1/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── schemas.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## ⚙️ Prerequisites

Install the following before running the project:

- Python 3.11 or newer
- Docker Desktop
- Git
- A GitHub account (optional, for hosting the repository)

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

Replace the URL with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

For local development, configure your database connection:

```env
DATABASE_URL=postgresql://todo_user:YOUR_PASSWORD@127.0.0.1:5433/todo_db
API_URL=http://127.0.0.1:8000
```

Replace `YOUR_PASSWORD` with the password configured for your PostgreSQL container.

**Important:** Never commit your `.env` file or actual credentials to GitHub.

### 5. Start PostgreSQL

Make sure Docker Desktop is running, then execute:

```powershell
docker compose -f compose.yml up -d
```

Check the container status:

```powershell
docker ps
```

Wait until PostgreSQL reports a healthy status.

### 6. Start the FastAPI backend

From the project root, run:

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

### 7. Explore the API documentation

Open:

`http://127.0.0.1:8000/docs`

Use Swagger UI to create, retrieve, update, and delete tasks.

### 8. Start the Streamlit frontend

Open a second terminal, activate the virtual environment, and run:

```powershell
streamlit run frontend/app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/todos` | Create a new task |
| GET | `/todos` | Retrieve all tasks |
| GET | `/todos/{todo_id}` | Retrieve a task by ID |
| PUT | `/todos/{todo_id}` | Update a task |
| DELETE | `/todos/{todo_id}` | Delete a task |

### Example: Create a Task

**Request**

```http
POST /todos
Content-Type: application/json
```

**Request body**

```json
{
  "title": "Learn FastAPI",
  "description": "Build my first REST API"
}
```

**Example response**

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Build my first REST API",
  "completed": false,
  "created_at": "2026-10-29T10:30:00"
}
```

The returned ID and timestamp will depend on your database.

## 🧪 Running Tests

Run the automated tests from the project root:

```powershell
python -m pytest -v
```

The test suite currently includes a health-check test. Additional tests for CRUD operations can be added as the project develops.

## 🐳 Docker

PostgreSQL is configured through Docker Compose.

Start the database:

```powershell
docker compose -f compose.yml up -d
```

Stop the database:

```powershell
docker compose -f compose.yml down
```

The database uses a Docker volume to persist its data.

**Note:** These commands manage the database service. Running the complete application in containers requires the API service to be configured in Docker Compose as well.

---

*Built as a hands-on project to strengthen software engineering and backend development skills.*