from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    """User model for authentication."""
    __tablename__ = "users"
    
    id: Optional[str] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    password: str  # Hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    tasks: list["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    """Task model for todo items."""
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")


# Pydantic models for API requests/responses

class UserCreate(SQLModel):
    """Schema for user registration."""
    email: str
    password: str
    name: str


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str
    password: str


class UserResponse(SQLModel):
    """Schema for user response (without password)."""
    id: str
    email: str
    name: str
    token: Optional[str] = None


class TaskCreate(SQLModel):
    """Schema for creating a task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None


class TaskResponse(SQLModel):
    """Schema for task response."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime