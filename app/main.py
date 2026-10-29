from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from app.database import (
    create_todo,
    delete_todo,
    get_all_todos,
    get_todo_by_id,
    initialize_database,
    update_todo,
)
from app.schemas import TodoCreate, TodoResponse, TodoUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Todo Management API",
    description="A REST API built with FastAPI and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_todo(todo: TodoCreate):
    return create_todo(
        title=todo.title,
        description=todo.description,
    )


@app.get("/todos", response_model=list[TodoResponse])
def read_all_todos():
    return get_all_todos()


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int):
    todo = get_todo_by_id(todo_id)

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def replace_todo(todo_id: int, todo: TodoUpdate):
    updated_todo = update_todo(
        todo_id=todo_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )

    if updated_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return updated_todo


@app.delete("/todos/{todo_id}")
def remove_todo(todo_id: int):
    deleted_todo = delete_todo(todo_id)

    if deleted_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return {
        "message": "Todo deleted successfully",
        "id": deleted_todo["id"],
    }