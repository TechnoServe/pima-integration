import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

DATABASE_URL = os.getenv("PG_PROD_DATABASE_URL")  # Local DB for development

if not DATABASE_URL:
    raise ValueError("PG_PROD_DATABASE_URL not set in environment")

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)

# Import Base AFTER engine is defined
from models import Base   # or adjust depending on where Base lives


def init_db():
    """Initialize the database (for development only)."""
    # Drop and recreate all tables
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    pass
