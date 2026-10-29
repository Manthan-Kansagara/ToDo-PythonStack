import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = (
    os.getenv("API_URL")
    or st.secrets["API_URL"]
).rstrip("/")

st.set_page_config(
    page_title="Todo Manager",
    page_icon="✅",
    layout="wide",
)

st.title("✅ Todo Management System")
st.caption("Create, view, edit, complete, and delete your tasks.")


def api_request(method, endpoint, **kwargs):
    """Send a request to the FastAPI backend."""

    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=10,
            **kwargs,
        )

        response.raise_for_status()

        if response.status_code == 204 or not response.content:
            return None

        return response.json()

    except requests.RequestException as error:
        st.error(f"API request failed: {error}")
        return None


# --------------------------------------------------
# CREATE: Add a new todo
# --------------------------------------------------

st.header("Create a new task")

with st.form("create_todo_form"):
    title = st.text_input("Task title")
    description = st.text_area("Task description")

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not title.strip():
            st.warning("Please enter a task title.")
        else:
            result = api_request(
                "POST",
                "/todos",
                json={
                    "title": title.strip(),
                    "description": description.strip(),
                },
            )

            if result is not None:
                st.success("Task created successfully!")
                st.rerun()


st.divider()


# --------------------------------------------------
# READ: Display all todos
# --------------------------------------------------

st.header("Your tasks")

todos = api_request("GET", "/todos")

if todos is not None:

    if not todos:
        st.info("No tasks found. Create your first task above.")

    for todo in todos:
        todo_id = todo["id"]

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                status_text = (
                    "✅ Completed"
                    if todo["completed"]
                    else "⏳ Pending"
                )

                st.subheader(todo["title"])
                st.caption(f"Task ID: {todo_id} | {status_text}")

                if todo["description"]:
                    st.write(todo["description"])

            with col2:

                # UPDATE: Toggle completion status
                button_label = (
                    "Mark Pending"
                    if todo["completed"]
                    else "Mark Completed"
                )

                if st.button(
                    button_label,
                    key=f"toggle_{todo_id}",
                    use_container_width=True,
                ):
                    result = api_request(
                        "PUT",
                        f"/todos/{todo_id}",
                        json={
                            "title": todo["title"],
                            "description": todo["description"] or "",
                            "completed": not todo["completed"],
                        },
                    )

                    if result is not None:
                        st.success("Task status updated!")
                        st.rerun()

                # DELETE: Remove a todo
                if st.button(
                    "Delete Task",
                    key=f"delete_{todo_id}",
                    use_container_width=True,
                ):
                    st.session_state["delete_todo_id"] = todo_id

            # ------------------------------------------
            # UPDATE: Edit the title and description
            # ------------------------------------------

            with st.expander("✏️ Edit Task"):

                with st.form(f"edit_form_{todo_id}"):

                    edited_title = st.text_input(
                        "Task title",
                        value=todo["title"],
                        key=f"edit_title_{todo_id}",
                    )

                    edited_description = st.text_area(
                        "Task description",
                        value=todo["description"] or "",
                        key=f"edit_description_{todo_id}",
                    )

                    edited_completed = st.checkbox(
                        "Task completed",
                        value=todo["completed"],
                        key=f"edit_completed_{todo_id}",
                    )

                    save_clicked = st.form_submit_button("Save Changes")

                    if save_clicked:

                        if not edited_title.strip():
                            st.warning("Task title cannot be empty.")

                        else:
                            result = api_request(
                                "PUT",
                                f"/todos/{todo_id}",
                                json={
                                    "title": edited_title.strip(),
                                    "description": edited_description.strip(),
                                    "completed": edited_completed,
                                },
                            )

                            if result is not None:
                                st.success("Task updated successfully!")
                                st.rerun()


# --------------------------------------------------
# DELETE: Confirm deletion
# --------------------------------------------------

if "delete_todo_id" in st.session_state:

    todo_id = st.session_state["delete_todo_id"]

    st.warning(
        f"Are you sure you want to delete task #{todo_id}?"
    )

    confirm_col, cancel_col = st.columns(2)

    with confirm_col:

        if st.button(
            "Yes, delete task",
            type="primary",
            key="confirm_delete",
        ):
            result = api_request(
                "DELETE",
                f"/todos/{todo_id}",
            )

            if result is not None:
                del st.session_state["delete_todo_id"]
                st.success("Task deleted successfully!")
                st.rerun()

    with cancel_col:

        if st.button(
            "Cancel",
            key="cancel_delete",
        ):
            del st.session_state["delete_todo_id"]
            st.rerun()