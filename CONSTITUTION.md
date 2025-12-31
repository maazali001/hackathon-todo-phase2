# Todo App Constitution - Phase II

## Project Vision
A modern, full-stack web application with authentication, persistent storage, and RESTful API architecture.

## Core Principles

### 1. Spec-Driven Development
- Every feature must have a specification before implementation
- Specifications are written in clear, executable language
- Claude Code generates implementation from specs

### 2. Full-Stack Architecture
- **Frontend**: Next.js 16+ with App Router
- **Backend**: Python FastAPI with RESTful API
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel for type-safe database operations
- **Auth**: Better Auth with JWT tokens

### 3. Security First
- All API endpoints require authentication
- JWT token-based authorization
- User data isolation (users only see their own tasks)
- Secure password handling

### 4. Code Quality Standards
- Clean, readable code in both frontend and backend
- Type safety (TypeScript + Python type hints)
- Proper error handling
- RESTful API conventions

## Technology Constraints

### Frontend
- Next.js 16+ (App Router, not Pages Router)
- TypeScript
- Tailwind CSS for styling
- Better Auth for authentication

### Backend
- Python 3.13+
- FastAPI framework
- SQLModel ORM
- Pydantic for validation
- JWT for token management

### Database
- Neon Serverless PostgreSQL
- Proper schema design
- Indexes for performance

## Feature Requirements

All Basic Level features from Phase I, now as web application:
1. ✅ User Authentication (signup/signin)
2. ✅ Add Task
3. ✅ Delete Task
4. ✅ Update Task
5. ✅ View Task List
6. ✅ Mark as Complete

## API Design

### RESTful Endpoints
```
GET    /api/{user_id}/tasks          - List all user tasks
POST   /api/{user_id}/tasks          - Create new task
GET    /api/{user_id}/tasks/{id}     - Get task details
PUT    /api/{user_id}/tasks/{id}     - Update task
DELETE /api/{user_id}/tasks/{id}     - Delete task
PATCH  /api/{user_id}/tasks/{id}/complete - Toggle completion
```

### Security
- All endpoints require valid JWT token in Authorization header
- Backend validates token and user_id match
- Database queries filtered by authenticated user

## Deployment Strategy
- Frontend: Vercel
- Backend: To be deployed
- Database: Neon cloud

## Success Criteria
- ✅ Working authentication system
- ✅ All CRUD operations functional
- ✅ Multi-user support with data isolation
- ✅ Responsive UI
- ✅ RESTful API following conventions
- ✅ Deployed and accessible via public URLs