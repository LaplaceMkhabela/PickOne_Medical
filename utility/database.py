from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///patients1.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    age = Column(String)
    gender = Column(String)
    bp = Column(String)
    weight = Column(String)
    bmi = Column(String)
    temp = Column(String)
    pulse = Column(String)
    bmp = Column(String)

Base.metadata.create_all(engine)


# ---- CRUD ----

def create_user(db, name, email,phone,age,gender,bp,weight,bmi,temp,pulse,bpm):
    user = User(name=name, email=email,phone=phone,age=age,gender=gender,bp=bp,weight=weight,bmi=bmi,temp=temp,pulse=pulse,bpm=bpm)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db, user_id, name=None, email=None):
    user = get_user(db, user_id)
    if not user:
        return None
    if name: user.name = name
    if email: user.email = email
    db.commit()
    return user

def delete_user(db, user_id):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


# Example usage
db = SessionLocal()
