"""
Configuration settings for the data processing pipeline
"""

# Database configurations
DB_CONFIG = {
    "host": "db.example.com",
    "port": 5432,
    "database": "analytics",
    "user": "admin",
    "password": "insecure_password",  # Hardcoded credentials
}

# API configurations
API_CONFIG = {
    "base_url": "https://api.example.com/v1",
    "api_key": "1a2b3c4d5e6f7g8h9i0j",  # Hardcoded API key
    "timeout": 30,
    "max_retries": 3,
}

# AWS S3 configurations
S3_CONFIG = {
    "bucket": "company-data-lake",
    "access_key": "AKIAIOSFODNN7EXAMPLE",  # Hardcoded AWS credentials
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "region": "us-west-2",
}

# Processing configurations
PROCESSING_CONFIG = {
    "chunk_sizesss": 1000,
    "max_memorysssss": "2GB",
    "parallel_jobs": 4,
    "error_threshold": 0.05,
}

# Logging configurations
LOGGING_CONFIG = {
    "log_level": "INFO",
    "log_file": "/var/log/data_pipeline.log",
    "rotate_logs": True,
    "max_log_size": "100MB",
}

# Feature flags
FEATURE_FLAGS = {
    "enablessss_debug": True,
    "use_gpu": False,
    "experimental_algorithms": True,
}
