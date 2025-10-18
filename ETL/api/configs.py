import os
from datetime import datetime

class Config:
    """Configuration settings for the Flask API"""
    
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2025'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Node-RED configuration
    NODE_RED_URL = os.environ.get('NODE_RED_URL', 'http://localhost:1880')
    NODE_RED_ENDPOINT = '/api/knime-data'
    NODE_RED_TIMEOUT = 30
    
    # API configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = f"logs/api_{datetime.now().strftime('%Y%m%d')}.log"

class DevelopmentConfig(Config):
    DEBUG = True
    NODE_RED_URL = 'http://localhost:1880'

class ProductionConfig(Config):
    DEBUG = False
    NODE_RED_URL = 'http://nodered:1880'  # Docker container name

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}