"""Package-specific database configuration."""
from core.db.base_db import setup_database

# Initialize with default configuration
DB_SCHEMA = "raw"  # Default schema for this package
db_config = setup_database(DB_SCHEMA)
engine = db_config['engine']
SessionLocal = db_config['SessionLocal']
Base = db_config['Base']  # pylint: disable=missing-final-newline