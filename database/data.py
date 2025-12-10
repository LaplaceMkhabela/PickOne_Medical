from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///instance/patients.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    age = Column(String, unique=False)
    gender = Column(String)
    bp = Column(String)
    weight = Column(String)
    bmi = Column(String)
    temp = Column(String)
    pulse = Column(String)
    hbpm = Column(String)
    history = Column(String)


def create_patient(
    db, name, email, age, gender, bp, weight, bmi, temp, pulse, hbpm, history
):
        
    p = Patient(
        name=name,
        email=email,
        age=str(age),
        gender=str(gender),
        bp=','.join(map(lambda num:str(num),bp)),
        weight=','.join(map(lambda num:str(num),weight)),
        bmi=','.join(map(lambda num:str(num),bmi)),
        temp=','.join(map(lambda num:str(num),temp)),
        pulse=','.join(map(lambda num:str(num),pulse)),
        hbpm=','.join(map(lambda num:str(num),hbpm)),
        history=history,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def get_patient(db, patient_id):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def update_patient(db, patient_id, name=None, email=None):
    p = get_patient(db, patient_id)
    if not p:
        return None
    if name:
        p.name = name
    if email:
        p.email = email
    db.commit()
    return p


def delete_patient(db, user_id):
    p = get_patient(db, user_id)
    if p:
        db.delete(p)
        db.commit()
        return True
    return False


patient_db = SessionLocal()
