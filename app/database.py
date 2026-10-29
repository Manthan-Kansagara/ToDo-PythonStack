import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Check your .env file."
    )


def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


def create_todo(title: str, description: str):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO todos (title, description)
                VALUES (%s, %s)
                RETURNING id, title, description, completed, created_at;
                """,
                (title, description),
            )

            return cursor.fetchone()


def get_all_todos():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, completed, created_at
                FROM todos
                ORDER BY id DESC;
                """
            )

            return cursor.fetchall()


def get_todo_by_id(todo_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, completed, created_at
                FROM todos
                WHERE id = %s;
                """,
                (todo_id,),
            )

            return cursor.fetchone()


def update_todo(
    todo_id: int,
    title: str,
    description: str,
    completed: bool,
):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE todos
                SET title = %s,
                    description = %s,
                    completed = %s
                WHERE id = %s
                RETURNING id, title, description, completed, created_at;
                """,
                (title, description, completed, todo_id),
            )

            return cursor.fetchone()


def delete_todo(todo_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM todos
                WHERE id = %s
                RETURNING id;
                """,
                (todo_id,),
            )

            return cursor.fetchone()