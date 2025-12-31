# Todo App - Phase II

A modern full-stack web application with user authentication and persistent storage, built using spec-driven development.

## 🚀 Features

### Authentication
- ✅ User Signup/Registration
- ✅ User Login
- ✅ JWT Token-based Authentication
- ✅ Secure Password Hashing (bcrypt)
- ✅ Session Management

### Task Management
- ✅ **Add Task** - Create new tasks with title and description
- ✅ **View Tasks** - Display all tasks with filtering (All/Pending/Completed)
- ✅ **Update Task** - Edit task title and description
- ✅ **Delete Task** - Remove tasks with confirmation
- ✅ **Toggle Complete** - Mark tasks as complete/incomplete
- ✅ **Multi-user Support** - Each user sees only their own tasks

## 🛠️ Technology Stack

### Frontend
- **Framework:** Next.js 16+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Authentication:** Better Auth
- **State Management:** React Hooks

### Backend
- **Framework:** Python FastAPI
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** JWT (python-jose)
- **Password Hashing:** bcrypt + passlib

### Development
- **Spec-Driven Development:** Claude Code + Spec-Kit Plus
- **Version Control:** Git & GitHub

## 📁 Project Structure
```
hackathon-todo-phase2/
├── frontend/                # Next.js frontend application
│   ├── app/                # App Router pages
│   │   ├── api/           # API routes (Better Auth)
│   │   ├── login/         # Login page
│   │   ├── signup/        # Signup page
│   │   ├── dashboard/     # Main todo dashboard
│   │   └── page.tsx       # Home page
│   ├── lib/               # Utility functions
│   │   ├── api.ts         # Backend API client
│   │   └── auth.ts        # Better Auth config
│   └── .env.local         # Environment variables
├── backend/               # FastAPI backend application
│   ├── main.py           # Main application & API routes
│   ├── models.py         # Database models (SQLModel)
│   ├── database.py       # Database connection
│   ├── auth.py           # Authentication utilities
│   └── .env              # Environment variables
├── specs/                # Specifications
│   ├── features/        # Feature specifications
│   ├── api/             # API endpoint specs
│   └── database/        # Database schema specs
├── CONSTITUTION.md       # Project rules and principles
└── README.md            # This file
```

## 🚦 Getting Started

### Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL database (Neon account)
- UV package manager

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/maazali001/hackathon-todo-phase2.git
cd hackathon-todo-phase2
```

#### 2. Backend Setup
```bash
cd backend

# Install dependencies
uv sync

# Create .env file with your database URL
echo "DATABASE_URL=your-neon-connection-string" > .env
echo "BETTER_AUTH_SECRET=your-secret-key" >> .env

# Run backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: http://localhost:8000

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "DATABASE_URL=your-neon-connection-string" > .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" >> .env.local
echo "BETTER_AUTH_SECRET=your-secret-key" >> .env.local
echo "BETTER_AUTH_URL=http://localhost:3000" >> .env.local

# Run frontend
npm run dev
```

Frontend will run on: http://localhost:3000

## 📡 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/signin` - Login user

### Tasks (Requires Authentication)
- `GET /api/{user_id}/tasks` - Get all tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get task by ID
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## 🔒 Security Features

- JWT token-based authentication
- Bcrypt password hashing
- User data isolation (users can only access their own tasks)
- Protected API endpoints
- Token expiration (7 days)
- CORS configured for frontend-backend communication

## 🎯 Development Approach

This project follows **Spec-Driven Development** principles:
1. Write specifications in `/specs`
2. Use Claude Code for implementation
3. Iterative development and testing

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key
```

### Frontend (.env.local)
```env
DATABASE_URL=postgresql://user:password@host/database
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:3000
```

## 🚀 Deployment

### Frontend (Vercel)
- Push code to GitHub
- Connect repository to Vercel
- Add environment variables
- Deploy automatically

### Backend
- Deploy to your preferred platform
- Update `NEXT_PUBLIC_API_URL` in frontend

### Database
- Already hosted on Neon Serverless PostgreSQL

## 📊 Database Schema

### Users Table
- `id` (UUID, primary key)
- `email` (unique)
- `name`
- `password` (hashed)
- `created_at`, `updated_at`

### Tasks Table
- `id` (integer, primary key)
- `user_id` (foreign key)
- `title` (max 200 chars)
- `description` (optional, max 1000 chars)
- `completed` (boolean)
- `created_at`, `updated_at`

## 👨‍💻 Author

**Maaz Ali**

Built as part of Panaversity Hackathon II - Phase II

## 📅 Timeline

- **Start Date:** December 1, 2025
- **Due Date:** December 14, 2025
- **Points:** 150

## 📜 License

MIT

## 🙏 Acknowledgments

- Panaversity Team
- PIAIC & GIAIC
- Claude Code by Anthropic
- Spec-Kit Plus