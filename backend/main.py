from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import Optional
import uuid

from database import create_db_and_tables, get_session, engine
from models import (
    User, Task, UserCreate, UserLogin, UserResponse,
    TaskCreate, TaskUpdate, TaskResponse
)
from auth import hash_password, verify_password, create_access_token, verify_token

app = FastAPI(title="Todo API - Phase II")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hackathon-todo-phase2-seven.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_db_and_tables()


# Auth endpoints

@app.post("/auth/signup", response_model=UserResponse)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        name=user_data.name,
        password=hash_password(user_data.password)
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Create JWT token
    token = create_access_token({"sub": user.id, "email": user.email})
    
    return UserResponse(id=user.id, email=user.email, name=user.name, token=token)


@app.post("/auth/signin", response_model=UserResponse)
def signin(user_data: UserLogin, session: Session = Depends(get_session)):
    """Login user."""
    # Find user
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    token = create_access_token({"sub": user.id, "email": user.email})
    
    return UserResponse(id=user.id, email=user.email, name=user.name, token=token)


# Helper function to verify JWT token
def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """Verify JWT token and return user_id."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload.get("sub")


# Task endpoints

@app.get("/api/{user_id}/tasks", response_model=list[TaskResponse])
def get_tasks(
    user_id: str,
    status: str = "all",
    authenticated_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for authenticated user."""
    # Verify user_id matches authenticated user
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Build query
    query = select(Task).where(Task.user_id == user_id)
    
    # Filter by status
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
    
    tasks = session.exec(query).all()
    return tasks


@app.post("/api/{user_id}/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    authenticated_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task."""
    # Verify user_id matches authenticated user
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@app.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: int,
    authenticated_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get specific task."""
    # Verify user_id matches authenticated user
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    task = session.get(Task, task_id)
    
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@app.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    authenticated_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a task."""
    # Verify user_id matches authenticated user
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    task = session.get(Task, task_id)
    
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    
    from datetime import datetime
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@app.delete("/api/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    authenticated_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task."""
    # Verify user_id matches authenticated user
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    task = session.get(Task, task_id)
    
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    
    return {"message": "Task deleted successfully", "id": task_id}


@app.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    authenticated_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle task completion status."""
    # Verify user_id matches authenticated user
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    task = session.get(Task, task_id)
    
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Toggle completion
    task.completed = not task.completed
    
    from datetime import datetime
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Todo API - Phase II", "status": "running"}