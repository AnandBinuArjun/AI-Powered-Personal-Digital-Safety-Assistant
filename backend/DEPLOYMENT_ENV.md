# Environment Variables Configuration for Deployment

This document explains how to configure environment variables for deploying the AI-Powered Personal Digital Safety Assistant to public testing.

## Environment Variables Setup

The application uses a `.env` file to manage configuration settings. This file should be located in the `backend` directory.

## Required Environment Variables

### Database Configuration
```bash
DB_HOST=localhost              # Database host
DB_PORT=5432                   # Database port
DB_NAME=safety_assistant       # Database name
DB_USER=postgres               # Database user
DB_PASSWORD=your_password      # Database password
```

### Security Settings
```bash
SECRET_KEY=your_secret_key_here_change_this_in_production     # App secret key
JWT_SECRET_KEY=your_jwt_secret_here_change_this_in_production # JWT secret
```

### Frontend URLs (for CORS)
```bash
FRONTEND_URL_LOCAL=http://localhost:3000                      # Local web app
FRONTEND_URL_ANDROID=http://localhost:3001                    # Android app
FRONTEND_URL_EXTENSION=chrome-extension://your-extension-id   # Browser extension
```

### Testing Configuration
```bash
DEBUG=True                     # Debug mode
TESTING=False                  # Testing mode
```

### Model Paths
```bash
MESSAGE_MODEL_PATH=models/message_model.pkl  # Message classifier model
URL_MODEL_PATH=models/url_model.pkl          # URL classifier model
```

## Optional Environment Variables for Production

### External API Keys
```bash
# HIBP API Key for breach detection
HIBP_API_KEY=your_haveibeenpwned_api_key_here

# Email service for notifications
SENDGRID_API_KEY=your_sendgrid_api_key
```

### Deployment Tokens
```bash
# Heroku deployment
HEROKU_API_KEY=your_heroku_api_key

# AWS deployment
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

## How to Configure for Public Testing

1. **Update Database Settings**
   - Change `DB_HOST` to your production database host
   - Update `DB_NAME`, `DB_USER`, and `DB_PASSWORD` with production credentials

2. **Update Security Keys**
   - Generate strong secret keys for `SECRET_KEY` and `JWT_SECRET_KEY`
   - Never commit actual keys to version control

3. **Configure Frontend URLs**
   - Update frontend URLs to match your deployed applications
   - For browser extensions, use the actual extension ID

4. **Add External Service Keys**
   - Obtain API keys for services like HIBP, SendGrid, etc.
   - Add them to the .env file

## Generating Strong Secret Keys

You can generate strong secret keys using Python:

```python
import secrets
print(secrets.token_urlsafe(32))
```

## Environment-Specific Configuration

For different environments, you can create separate files:
- `.env.development` - For local development
- `.env.staging` - For staging environment
- `.env.production` - For production environment

Then load the appropriate file in your application.

## Security Best Practices

1. **Never commit .env files to version control**
   - Add `.env` to your `.gitignore` file
   - Share configuration templates instead (`.env.example`)

2. **Use different keys for different environments**
   - Development, staging, and production should have different keys

3. **Rotate keys regularly**
   - Change secret keys periodically
   - Update API keys when they expire

4. **Restrict file permissions**
   - Set appropriate file permissions on the .env file
   - Limit access to only necessary processes

## Testing the Configuration

To verify that environment variables are loaded correctly:

```bash
cd backend
python verify_env.py
```

This will display all configured environment variables (masking sensitive values).

## Deployment Platforms

### Heroku
1. Set config vars in Heroku dashboard
2. Or use Heroku CLI: `heroku config:set KEY=VALUE`

### AWS
1. Set environment variables in Elastic Beanstalk configuration
2. Or use AWS Systems Manager Parameter Store

### Google Cloud Platform
1. Set environment variables in App Engine configuration
2. Or use Secret Manager for sensitive values

## Troubleshooting

### Common Issues
1. **Variables not loading**: Ensure `.env` file is in the correct directory
2. **Permission denied**: Check file permissions on `.env` file
3. **Invalid values**: Verify all values are properly quoted

### Debugging
1. Check that `python-dotenv` is installed
2. Verify the `.env` file path
3. Use `verify_env.py` to check loaded variables