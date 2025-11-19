import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "safety_assistant")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def init_db():
    """Initialize database tables."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                privacy_mode BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create scan_history table with privacy features
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                scan_type VARCHAR(20) NOT NULL,
                content_hash VARCHAR(64),  -- Store hash instead of raw content for privacy
                content_preview TEXT,      -- Small preview for user reference
                result JSONB,
                is_anonymized BOOLEAN DEFAULT FALSE,  -- Indicates if content was anonymized
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                scan_id INTEGER REFERENCES scan_history(id),
                is_correct BOOLEAN,
                comment TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create privacy_settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS privacy_settings (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) UNIQUE,
                store_raw_content BOOLEAN DEFAULT FALSE,
                share_anonymous_data BOOLEAN DEFAULT TRUE,
                auto_delete_after_days INTEGER DEFAULT 365,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def save_scan_result(user_id: int, scan_type: str, content: str, result: dict, privacy_mode: bool = False):
    """Save scan result with privacy-preserving options."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Handle privacy mode
        content_hash = None
        content_preview = None
        is_anonymized = False
        
        if privacy_mode or scan_type in ['message', 'url']:
            # Store hash instead of raw content
            import hashlib
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            # Store only a small preview for user reference
            content_preview = content[:50] + "..." if len(content) > 50 else content
            is_anonymized = True
        else:
            # For non-sensitive data, we can store more
            content_preview = content[:100] + "..." if len(content) > 100 else content
        
        # Insert scan result
        cursor.execute("""
            INSERT INTO scan_history 
            (user_id, scan_type, content_hash, content_preview, result, is_anonymized)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (user_id, scan_type, content_hash, content_preview, 
              psycopg2.extras.Json(result), is_anonymized))
        
        scan_id = cursor.fetchone()['id']
        conn.commit()
        cursor.close()
        conn.close()
        
        return scan_id
    except Exception as e:
        print(f"Error saving scan result: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

def get_user_privacy_settings(user_id: int):
    """Get user privacy settings."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT store_raw_content, share_anonymous_data, auto_delete_after_days
            FROM privacy_settings 
            WHERE user_id = %s
        """, (user_id,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            return dict(result)
        else:
            # Return default settings
            return {
                "store_raw_content": False,
                "share_anonymous_data": True,
                "auto_delete_after_days": 365
            }
    except Exception as e:
        print(f"Error getting privacy settings: {e}")
        if conn:
            conn.close()
        return None

def update_user_privacy_settings(user_id: int, settings: dict):
    """Update user privacy settings."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if settings exist
        cursor.execute("SELECT id FROM privacy_settings WHERE user_id = %s", (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing settings
            cursor.execute("""
                UPDATE privacy_settings 
                SET store_raw_content = %s, share_anonymous_data = %s, auto_delete_after_days = %s, updated_at = NOW()
                WHERE user_id = %s
            """, (settings.get('store_raw_content', False), 
                  settings.get('share_anonymous_data', True),
                  settings.get('auto_delete_after_days', 365),
                  user_id))
        else:
            # Insert new settings
            cursor.execute("""
                INSERT INTO privacy_settings 
                (user_id, store_raw_content, share_anonymous_data, auto_delete_after_days)
                VALUES (%s, %s, %s, %s)
            """, (user_id, settings.get('store_raw_content', False), 
                  settings.get('share_anonymous_data', True),
                  settings.get('auto_delete_after_days', 365)))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating privacy settings: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False