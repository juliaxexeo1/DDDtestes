from app.extensions import db,jwt
import bcrypt
from flask_jwt_extended import create_access_token

class Paciente(db.Model):
    __tablename__='paciente'
    id=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String(30),nullable=False)
    cpf=db.Column(db.String(11),nullable=False, unique=True)
    data_de_nascimento=db.Column(db.String,nullable=False)
    email=db.Column(db.String(100),nullable=False, unique=True)
    senha_hash = db.Column(db.String(300),nullable=False)

   
    
    def json(self):
        return{
        'nome':self.nome,
        'cpf':self.cpf,
        'data_de_nascimento':self.data_de_nascimento,
        'email':self.email}

    

    @property
    def senha(self):
        raise AttributeError('password is not a readable attribute')

    @senha.setter
    def senha(self, senha) -> None:
        self.senha_hash = bcrypt.hashpw(
            senha.encode(), bcrypt.gensalt())

    def verify_password(self, senha: str) -> bool:
        return bcrypt.checkpw(senha.encode(), self.senha_hash)

    def token(self) -> str:
        return create_access_token(
            identity=self.id)
