from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# importujeme env pomoci os.environ
from os import environ 

# env jsou nejednodussim zpusobem, jak nastavit parametry
# a ty se nactou
DB_USER = environ("DB_USER", "postgres") # pokud neni nastaveno, tak dam vychozi hodnotu - postgres
DB_PASSWORD = environ("DB_PASSWORD", "secret")
DB_SERVER = environ("DB_SERVER", "postgres")
DB_DATABASE = environ("DB_DATABASE", "pet_clinic")
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"

# Pripojeni k db
engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Ted vytvorime session z engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Case objekt pro deklaraci db objektu
Base = declarative_base()