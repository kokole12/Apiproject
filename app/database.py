from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
from sqlalchemy.orm import sessionmaker

sql_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(url=sql_url)

session = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

"""
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user="postgres",
                                    password="password123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("connection failed")
        print({"error": error})
        time.sleep(2)
"""
