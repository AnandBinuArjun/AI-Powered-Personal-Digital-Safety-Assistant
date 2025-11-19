# System Architecture - AI-Powered Personal Digital Safety Assistant

## Overview

The AI-Powered Personal Digital Safety Assistant is a comprehensive cybersecurity solution designed to protect users across multiple platforms through a unified backend system with machine learning capabilities.

## High-Level Architecture

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

## Backend API (FastAPI)

### Core Services

#### 1. Authentication Service
- User registration and login
- Password hashing with bcrypt
- JWT token generation and validation
- Session management

#### 2. Message Analysis Service
- Natural Language Processing for scam detection
- TF-IDF vectorization and feature extraction
- Multiple ML models (Naive Bayes, SVM, LSTM, BERT)
- Explainable AI with feature importance

#### 3. URL Analysis Service
- Lexical and host-based feature extraction
- Entropy calculation, subdomain analysis
- Suspicious keyword detection
- Integration with threat intelligence feeds

#### 4. Breach Detection Service
- Email breach checking with HIBP-style API
- Password safety using k-anonymity protocol
- Credential reuse detection

#### 5. Risk Scoring Engine
- Dynamic personal cyber safety score calculation
- Weighted risk factors
- Visual status indicators (green/yellow/red)
- Historical trend analysis

### API Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Authenticate user and return JWT

#### Scanning
- `POST /scan/analyze` - Analyze content (message, URL, email, password)
- `POST /scan/feedback` - Submit feedback for model improvement
- `GET /scan/history` - Retrieve scan history

#### Risk Scoring
- `GET /risk/score` - Get current user's risk score
- `GET /risk/score/{user_id}` - Get specific user's risk score

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Scan History Table
```sql
CREATE TABLE scan_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    scan_type VARCHAR(20) NOT NULL,
    content TEXT,
    result JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Feedback Table
```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    scan_id INTEGER REFERENCES scan_history(id),
    is_correct BOOLEAN,
    comment TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Machine Learning Models

### Message Classification
- **Preprocessing**: Tokenization, stopword removal, TF-IDF
- **Algorithms**: Naive Bayes, SVM, LSTM, BERT
- **Training Data**: SMS spam datasets, phishing email corpora
- **Explainability**: SHAP and feature importance analysis

### URL Classification
- **Features**: URL length, entropy, subdomain count, suspicious keywords
- **Algorithms**: Decision trees, Random Forest, XGBoost
- **Integration**: Threat intelligence feeds (OpenPhish-style)

## Android App (Flutter)

### Key Features
- User authentication
- Message scanning
- URL checking
- Breach monitoring
- Safety score display
- Push notifications

### Architecture
- Clean architecture with separation of concerns
- HTTP client for backend communication
- Secure token storage using Android Keystore
- Local caching for offline functionality

## Web Dashboard (React)

### Key Features
- User authentication
- Interactive charts for risk visualization
- Scan history display
- Detailed analytics
- Account management

### Technology Stack
- React with functional components and hooks
- Chart.js for data visualization
- Axios for HTTP requests
- CSS Modules for styling

## Browser Extension

### Key Features
- Current page analysis
- Context menu link scanning
- Automatic warning banners
- Safety score display in popup
- Real-time protection

### Implementation
- Manifest V3 compliance
- Content scripts for page interaction
- Background service worker for event handling
- Chrome APIs for notifications and context menus

## Security Implementation

### API Security
- HTTPS/TLS encryption
- JWT-based authentication
- Rate limiting
- Input sanitization and validation

### Data Privacy
- Privacy mode option
- Anonymized metadata storage
- K-anonymity for password checks
- Role-based database access control

## Deployment Architecture

### Backend Services
- FastAPI application deployed with Uvicorn
- PostgreSQL database
- Reverse proxy (nginx) for SSL termination
- Containerization with Docker (optional)

### Frontend Services
- Web dashboard deployed to static hosting (AWS S3, Netlify, etc.)
- Android app published to Google Play Store
- Browser extension published to Chrome Web Store

## Scalability Considerations

### Horizontal Scaling
- Load balancing for backend API
- Database read replicas
- CDN for static assets
- Caching layer (Redis)

### Performance Optimization
- Database indexing
- Query optimization
- Asynchronous processing for ML inference
- Connection pooling

## Monitoring and Maintenance

### Logging
- Structured logging for all services
- Error tracking and alerting
- Performance metrics collection

### Model Retraining
- Automated retraining pipeline
- A/B testing for model versions
- Feedback loop from user corrections

## Future Enhancements

1. **Advanced ML Models**: Integration of transformer-based models for better accuracy
2. **Real-time Protection**: WebSocket-based real-time threat detection
3. **Mobile Features**: Biometric authentication, push notifications
4. **Enterprise Features**: Admin dashboard, team management
5. **IoT Integration**: Extension to smart home devices
6. **Behavioral Analysis**: User behavior anomaly detection