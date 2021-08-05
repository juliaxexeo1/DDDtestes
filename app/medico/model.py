from app.extensions import db

class Medico(db.Model):
    __tablename__='medico'
    id=db.Column(db.Integer, primary_key=True)
    nome=db.Column(db.String(100),nullable=False)
    cpf=db.Column(db.String(30),nullable=False, unique=True)
    especialidade=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False, unique=True)
    senha_hash = db.Column(db.LargeBinary(128))

    def json(self):
        return{
        'nome':self.nome,
        'cpf':self.cpf,
        'especialidade':self.especialidade,
        'email':self.email}