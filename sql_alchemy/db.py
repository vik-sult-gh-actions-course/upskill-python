"""Package-specific database configuration."""

from core.db.base_db import setup_database

# Initialize with default configuration
db_config = setup_database()
engine = db_config["engine"]
SessionLocal = db_config["SessionLocal"]
Base = db_config["Base"]
