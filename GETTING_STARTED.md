# Getting Started with AI-Powered Personal Digital Safety Assistant

This document provides step-by-step instructions to set up and run the complete system.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js and npm
- PostgreSQL database
- Flutter SDK (for Android app development)
- Git (optional, for version control)

## Backend Setup

### 1. Install Essential Dependencies

Run the setup script to install the essential Python packages:

```bash
cd "c:\Users\anand\Downloads\AI-Powered Personal Digital Safety Assistant"
python setup_backend.py
```

Alternatively, you can manually install the dependencies:

```bash
pip install fastapi uvicorn[standard] pydantic psycopg2-binary python-jose passlib bcrypt python-multipart
```

### 2. Configure Database

Install PostgreSQL if you haven't already, then create a database:

```sql
CREATE DATABASE safety_assistant;
CREATE USER safety_user WITH PASSWORD 'safety_password';
GRANT ALL PRIVILEGES ON DATABASE safety_assistant TO safety_user;
```

Set environment variables for database configuration:

Windows (Command Prompt):
```cmd
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=safety_assistant
set DB_USER=safety_user
set DB_PASSWORD=safety_password
set SECRET_KEY=your_secret_key_here
```

Windows (PowerShell):
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="safety_assistant"
$env:DB_USER="safety_user"
$env:DB_PASSWORD="safety_password"
$env:SECRET_KEY="your_secret_key_here"
```

### 3. Initialize Database

Run the initialization script to set up database tables:

```bash
cd backend
python init_project.py
```

### 4. Run the Backend Server

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Web Dashboard Setup

### 1. Install Dependencies

```bash
cd web
npm install
```

### 2. Run the Development Server

```bash
npm start
```

The web dashboard will be available at `http://localhost:3000`

## Android App Setup

### 1. Install Flutter Dependencies

```bash
cd android
flutter pub get
```

### 2. Run the App

Connect an Android device or start an emulator, then run:

```bash
flutter run
```

## Browser Extension Setup

### 1. Install in Chrome/Edge

1. Open Chrome/Edge and navigate to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` directory

## System Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Android App   │    │  Web Dashboard   │    │ Browser Extension│
│    (Flutter)    │    │     (React)      │    │   (JavaScript)   │
└─────────┬───────┘    └────────┬─────────┘    └────────┬─────────┘
          │                     │                       │
          └─────────────────────┼───────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │    Backend API        │
                    │     (FastAPI)         │
                    ├───────────────────────┤
                    │  Authentication       │
                    │  Message Analysis     │
                    │  URL Analysis         │
                    │  Breach Detection     │
                    │  Risk Scoring         │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │     PostgreSQL        │
                    │     Database          │
                    └───────────────────────┘
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Scanning
- `POST /scan/analyze` - Analyze content (message, URL, email, password)
- `POST /scan/feedback` - Submit feedback for scan results
- `GET /scan/history` - Get scan history

### Risk Scoring
- `GET /risk/score` - Get current risk score
- `GET /risk/score/{user_id}` - Get risk score for specific user

## Development Guidelines

### Backend Development
1. Follow the existing code structure
2. Use Pydantic models for request/response validation
3. Implement proper error handling
4. Write unit tests for new functionality

### Web Development
1. Use functional components with hooks
2. Follow CSS module conventions
3. Implement proper error boundaries
4. Use Axios for API calls

### Mobile Development
1. Follow Flutter best practices
2. Use proper state management
3. Implement responsive design
4. Follow platform-specific guidelines

### Extension Development
1. Follow Manifest V3 specifications
2. Use Chrome APIs appropriately
3. Implement proper error handling
4. Test across different browsers

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check if PostgreSQL is running
   - Verify database credentials
   - Ensure environment variables are set correctly

2. **Module Not Found Errors**
   - Run `pip install -r requirements.txt` in the backend directory
   - Ensure you're using the correct Python environment

3. **Port Already in Use**
   - Change the port in the uvicorn command: `uvicorn main:app --port 8001 --reload`

4. **Flutter Build Issues**
   - Run `flutter doctor` to check for issues
   - Ensure Android SDK is properly installed

### Getting Help

- Check the API documentation at `http://localhost:8000/docs`
- Review the code comments for implementation details
- Refer to the PROJECT_SUMMARY.md for architectural overview

## Next Steps

1. Implement machine learning models for message and URL analysis
2. Integrate with real threat intelligence feeds
3. Add more comprehensive analytics to the web dashboard
4. Implement push notifications for the mobile app
5. Add more security features like two-factor authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request