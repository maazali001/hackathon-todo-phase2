# Database Schema

## Tables

### users (managed by Better Auth)
Better Auth automatically creates and manages the users table.

**Fields:**
- `id`: string (primary key, UUID)
- `email`: string (unique, not null)
- `name`: string
- `password`: string (hashed)
- `created_at`: timestamp
- `updated_at`: timestamp

### tasks

**Fields:**
- `id`: integer (primary key, auto-increment)
- `user_id`: string (foreign key -> users.id, not null)
- `title`: string (max 200 chars, not null)
- `description`: text (nullable)
- `completed`: boolean (default: false)
- `created_at`: timestamp (default: now)
- `updated_at`: timestamp (default: now, auto-update)

## Indexes
```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

## Relationships

- **users** 1 → many **tasks**
- Each task belongs to exactly one user
- Cascade delete: when user deleted, all their tasks deleted

## Constraints

- `tasks.user_id` must reference valid `users.id`
- `tasks.title` cannot be empty or null
- `tasks.completed` defaults to false

## Sample Data Structure

### User
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john@example.com",
  "name": "John Doe",
  "created_at": "2025-01-01T00:00:00Z"
}
```

### Task
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```