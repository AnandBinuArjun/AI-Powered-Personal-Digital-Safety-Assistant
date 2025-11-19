# AI-Powered Personal Digital Safety Assistant
## Master's-Level Cybersecurity Solution

A comprehensive, multi-platform cybersecurity solution that protects users across Android, web browsers, and desktop environments using AI-powered threat detection and a unified backend system.

## 🏗️ System Architecture Overview

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

## 🚀 Key Features

### 🔍 Scam and Phishing Detection
- **Message Analysis**: NLP-based detection using TF-IDF and machine learning models
- **URL Risk Assessment**: Lexical and host-based feature extraction
- **Explainable AI**: SHAP and feature importance for transparent predictions

### 🛡️ Breach and Password Safety
- **Email Breach Detection**: Integration with HIBP-style API
- **Password Safety**: K-anonymity protocol for secure checking
- **Credential Monitoring**: Detection of reused or compromised credentials

### 📊 Risk Scoring Engine
- **Dynamic Safety Score**: Personalized cyber safety rating (0-100)
- **Weighted Factors**: Breach history, malicious links, suspicious messages, password reuse
- **Visual Indicators**: Green (safe), Yellow (moderate risk), Red (high risk)
- **User Feedback**: Continuous model improvement through user corrections

## 🎓 Advanced Master's-Level Features

### 1. Explainable AI (XAI)
- **SHAP Integration**: Detailed feature contribution analysis
- **Feature Importance**: Transparent model decision-making
- **Human-Readable Explanations**: Natural language threat descriptions

### 2. Privacy-Preserving Design
- **Content Hashing**: SHA-256 hashing instead of raw content storage
- **Granular Privacy Controls**: User-configurable data sharing settings
- **Data Minimization**: Store only necessary information
- **Auto-Deletion**: Configurable data retention policies

### 3. Feedback Loop for Continuous Learning
- **Dedicated Feedback Storage**: Database table for user corrections
- **UI Integration**: Feedback mechanisms in all client interfaces
- **False Positive/Negative Tracking**: Specific model improvement tracking

### 4. Cross-Platform Consistency
- **Unified Risk Engine**: Single scoring algorithm across all platforms
- **Consistent Detection**: Same threat analysis regardless of interface
- **Platform Insights**: Usage analytics by device type

## 🛠️ Technology Stack

### Backend (Python/FastAPI)
- **Framework**: FastAPI for high-performance REST API
- **Database**: PostgreSQL with JSONB for flexible data storage
- **ML Libraries**: Scikit-learn, PyTorch, XGBoost, SHAP
- **Security**: JWT authentication, bcrypt password hashing
- **Deployment**: Uvicorn ASGI server

### Frontend Technologies
- **Android App**: Flutter with Dart
- **Web Dashboard**: React with Chart.js
- **Browser Extension**: JavaScript (Manifest V3)

## 📁 Project Structure

```
AI-Powered-Personal-Digital-Safety-Assistant/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── .env.example            # Environment variable template
│   ├── init_project.py         # Database initialization
│   ├── routes/                 # API route handlers
│   │   ├── auth_routes.py      # Authentication endpoints
│   │   ├── scan_routes.py      # Scanning endpoints
│   │   └── risk_routes.py      # Risk scoring endpoints
│   ├── services/               # Business logic
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── breach_service.py   # Breach detection
│   │   └── risk_service.py     # Risk scoring engine
│   ├── models/                 # Machine learning models
│   │   ├── base_model.py       # Abstract model base class
│   │   ├── message_classifier.py # Message analysis ML model
│   │   └── url_classifier.py   # URL analysis ML model
│   ├── schemas/                # Pydantic data models
│   │   ├── auth.py             # Authentication schemas
│   │   └── scan.py             # Scanning schemas
│   └── utils/                  # Utility functions
│       └── database.py         # Database connection utilities
├── android/
│   ├── lib/
│   │   ├── main.dart           # App entry point
│   │   └── screens/
│   │       └── home_screen.dart # Main app screens
│   └── pubspec.yaml            # Flutter dependencies
├── web/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── index.js            # Entry point
│   │   └── components/
│   │       ├── Dashboard.js    # Dashboard component
│   │       └── Login.js        # Authentication component
│   └── package.json            # NPM dependencies
├── extension/
│   ├── manifest.json           # Extension metadata
│   ├── popup.html              # Extension popup UI
│   ├── popup.js                # Popup functionality
│   ├── content.js              # Content script for web pages
│   └── background.js           # Background service worker
└── README.md                   # Project documentation
```

## 🧠 Machine Learning Models

### Message Classifier
- **Algorithms**: Naive Bayes, SVM, LSTM, BERT
- **Preprocessing**: Tokenization, stopword removal, TF-IDF
- **Training Data**: SMS spam datasets, phishing email corpora
- **Explainability**: SHAP values and feature importance

### URL Classifier
- **Algorithms**: Decision trees, Random Forest, XGBoost
- **Features**: URL length, entropy, subdomain count, suspicious keywords
- **Integration**: Threat intelligence feeds (OpenPhish-style)
- **Analysis**: Lexical and host-based feature extraction

## 🔐 Security Implementation

### API Security
- **HTTPS/TLS**: All communication encrypted
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Prevention of API abuse
- **Input Validation**: Protection against injection attacks

### Data Privacy
- **Privacy Mode**: User-toggleable detailed content storage
- **Content Hashing**: SHA-256 for privacy-preserving storage
- **Data Minimization**: Store only necessary information
- **User Control**: Full control over personal data

### Database Security
- **Role-Based Access**: Proper user permissions
- **Password Hashing**: bcrypt for secure password storage
- **Connection Security**: SSL/TLS database connections
- **Audit Logging**: Track API usage for security oversight

## 🌐 API Endpoints

### Authentication
```
POST /auth/register     # Register new user
POST /auth/login        # User authentication
POST /auth/refresh      # Refresh access token
```

### Scanning Services
```
POST /scan/analyze      # Analyze content (message, URL, email, password)
POST /scan/feedback     # Submit user feedback
GET  /scan/history      # Retrieve scan history
GET  /scan/privacy-settings # Get privacy settings
POST /scan/privacy-settings # Update privacy settings
```

### Risk Scoring
```
GET /risk/score         # Get current user risk score
GET /risk/score/{user_id} # Get specific user risk score
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    privacy_mode BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Scan History Table
```sql
CREATE TABLE scan_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    scan_type VARCHAR(20) NOT NULL,
    content_hash VARCHAR(64),  -- SHA-256 hash for privacy
    content_preview TEXT,      -- Limited content preview
    result JSONB,              -- Scan results in JSON format
    is_anonymized BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Feedback Table
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

### Privacy Settings Table
```sql
CREATE TABLE privacy_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    store_raw_content BOOLEAN DEFAULT FALSE,
    share_anonymous_data BOOLEAN DEFAULT TRUE,
    auto_delete_after_days INTEGER DEFAULT 365,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Getting Started

### Backend Setup
1. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   # Copy example file and update with your values
   cp .env.example .env
   ```

3. **Initialize Database**:
   ```bash
   python init_project.py
   ```

4. **Run Server**:
   ```bash
   uvicorn main:app --reload
   ```

### Web Dashboard Setup
1. **Install Dependencies**:
   ```bash
   cd web
   npm install
   ```

2. **Run Development Server**:
   ```bash
   npm start
   ```

### Android App Setup
1. **Install Dependencies**:
   ```bash
   cd android
   flutter pub get
   ```

2. **Run App**:
   ```bash
   flutter run
   ```

### Browser Extension Setup
1. Open Chrome/Edge and navigate to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` directory

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Web Dashboard Testing
```bash
cd web
npm test
```

### Android App Testing
```bash
cd android
flutter test
```

## ☁️ Deployment

### Backend Deployment Options
1. **Heroku**:
   ```bash
   heroku create
   git push heroku main
   ```

2. **AWS Elastic Beanstalk**:
   ```bash
   eb init
   eb create
   eb deploy
   ```

3. **Google Cloud Run**:
   ```bash
   gcloud run deploy
   ```

### Frontend Deployment
1. **Web Dashboard**:
   ```bash
   cd web
   npm run build
   # Deploy build/ directory to static hosting
   ```

2. **Android App**:
   - Build APK: `flutter build apk`
   - Publish to Google Play Store

3. **Browser Extension**:
   - Package extension
   - Publish to Chrome Web Store

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast (high-performance) web framework
- [Scikit-learn](https://scikit-learn.org/) - Machine learning in Python
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Flutter](https://flutter.dev/) - UI toolkit for building natively compiled applications
- [SHAP](https://github.com/slundberg/shap) - Game theoretic approach to explain ML models

## 📞 Support

For support, email support@safetyassistant.com or join our [Discord community](https://discord.gg/safetyassistant).

---

<p align="center">
  <strong>🛡️ Protecting users across all digital platforms 🛡️</strong>
</p>