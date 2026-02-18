from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "saans_portal"

# DATABASE_URL = "mysql+pymysql://root:@localhost:3306/saans_portal"
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/saans_portal"
# DATABASE_URL = "mysql+pymysql://phpmyadmin:kreate%40123@localhost:3306/saas_master"


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Connection test function
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        return str(e)
