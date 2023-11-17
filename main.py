from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

#commit clainer

DATABASE_URL = "mysql+mysqlconnector://root:@127.0.0.1:3306/db_ajuda_ai"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
# Model para usuário
class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(255), unique=True, index=True)
    email = Column(String(255), index=True)
    password = Column(String(255))
    name = Column(String(255))

# Model para serviço
class Service(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    service_name = Column(String(255))
    value = Column(Float)
    description = Column(String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_name": self.service_name,
            "value": self.value,
            "description": self.description,
        }
# Criar tabelas
metadata = MetaData()
Base.metadata.create_all(bind=engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas
@app.post("/register")
def register_user(cpf: str, email: str, password: str, name: str, db: Session = Depends(get_db)):
    user = User(cpf=cpf, email=email, password=password, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/login")
def login_user(cpf: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.cpf == cpf, User.password == password).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Login unsuccessful")
    return {"message": "Login successful"}

@app.post("/services")
def create_service(service_name: str, value: float, description: str, user_id: int, db: Session = Depends(get_db)):
    service = Service(service_name=service_name, value=value, description=description, user_id=user_id)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@app.get("/services")
def get_services(user_id: int, db: Session = Depends(get_db)):
    services = db.query(Service).filter(Service.user_id == user_id).all()
    return services

# Adicione esta rota ao final do seu código

@app.get("/all-services", response_model=List[dict])
def get_all_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return [service.to_dict() for service in services]
