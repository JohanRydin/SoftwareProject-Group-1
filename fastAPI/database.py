from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:root@db:3306/storage"

# SQLAlchemy engine and session setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


TEST_DATABASE_URL = "sqlite:///:memory:"  # In-memory SQLite for testing

test_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
test_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to switch to test database in tests
def get_test_db():
    test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

