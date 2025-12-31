# REST API Endpoints

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-backend-url.com`

## Authentication
All endpoints (except auth endpoints) require JWT token in header:
```
Authorization: Bearer <jwt_token>
```

## Auth Endpoints

### POST /auth/signup
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "jwt_token_here"
}
```

### POST /auth/signin
Login with existing account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "jwt_token_here"
}
```

## Task Endpoints

### GET /api/{user_id}/tasks
List all tasks for authenticated user.

**Query Parameters:**
- `status`: "all" | "pending" | "completed" (optional, default: "all")
- `sort`: "created" | "title" | "updated" (optional, default: "created")

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": "user_id",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-01-01T10:00:00Z",
    "updated_at": "2025-01-01T10:00:00Z"
  }
]
```

### POST /api/{user_id}/tasks
Create a new task.

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": "user_id",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

### GET /api/{user_id}/tasks/{id}
Get specific task details.

**Response (200):**
```json
{
  "id": 1,
  "user_id": "user_id",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

### PUT /api/{user_id}/tasks/{id}
Update a task.

**Request Body:**
```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples"
}
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": "user_id",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples",
  "completed": false,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

### DELETE /api/{user_id}/tasks/{id}
Delete a task.

**Response (200):**
```json
{
  "message": "Task deleted successfully",
  "id": 1
}
```

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle task completion status.

**Response (200):**
```json
{
  "id": 1,
  "user_id": "user_id",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T14:00:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing authentication token"
}
```

### 403 Forbidden
```json
{
  "detail": "You don't have permission to access this resource"
}
```

### 404 Not Found
```json
{
  "detail": "Task not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Security Notes
- All requests must include valid JWT token (except auth endpoints)
- Backend validates that JWT user_id matches URL user_id
- Users can only access their own tasks
- Token expires after 7 days