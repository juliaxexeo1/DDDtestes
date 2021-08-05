from flask.wrappers import Request
from app.paciente.model import Paciente
from flask import request,jsonify
from flask.views import MethodView
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils import testa_email, testa_cpf


import bcrypt

class PacienteCreate(MethodView):#'/cliente/create'
    

    def get(self):
        paciente = Paciente.query.all()
        return jsonify ([paciente.json()for paciente in paciente]),200

    def post(self):

        dados = request.json

        nome = dados.get('nome')
        cpf = dados.get('cpf')
        data_de_nascimento = dados.get('data_de_nascimento')
        email = dados.get('email')
        senha = dados.get('senha')

        #validação de dados
        if not isinstance(nome,str): 
            return{'error':'nome invalido'},400
        elif not testa_cpf(cpf):
            return{'error':'cpf invalido'},400
        elif not isinstance(data_de_nascimento,str):
            return{'error':'data_de_nascimento invalido'},400
        elif not testa_email (email):
            return{'error':'email invalido'},400
        
        paciente = Paciente.query.filter_by(email = email).first()

        if paciente:
            return {'error':'Email já cadastrado'},400

        paciente = Paciente.query.filter_by(cpf = cpf).first()

        if paciente:
            return {'error':'CPF já cadastrado'},400






        #senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())

        paciente = Paciente(nome=nome,cpf=cpf,data_de_nascimento=data_de_nascimento,email=email)
        paciente.senha=senha
        db.session.add(paciente)
        db.session.commit()

        

        return paciente.json(),200

class PacienteDetails(MethodView):#'/paciente/details/<int:id>'

    decorators = [jwt_required()]
   
    def get (self,id):

        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400
        
        paciente = Paciente.query.get_or_404(id)
        return paciente.json(),200
    
 
    def put (self,id):
        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400

        paciente = Paciente.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome')
        cpf = dados.get('cpf')
        data_de_nascimento = dados.get('data_de_nascimento')
        email = dados.get('email')
        senha = dados.get('senha')

       



         #validação de dados
        if not isinstance(nome,str): 
            return{'error':'nome invalido'},400
        elif not  testa_cpf(cpf):
            return{'error':'cpf invalido'},400
        elif not isinstance(data_de_nascimento,str):
            return{'error':'data_de_nascimento invalido'},400
        elif not testa_email (email):
            return{'error':'email invalido'},400


        senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())
        

        paciente.nome = nome
        paciente.cpf = cpf
        paciente.data_de_nascimento = data_de_nascimento
        paciente.email = email
        paciente.senha_hash = senha_hash

        db.session.commit()

        return paciente.json(),200
    

    def patch(self,id):

        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400

        paciente = Paciente.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome',paciente.nome)
        cpf = dados.get('cpf',paciente.cpf)
        data_de_nascimento = dados.get('data_de_nascimento',paciente.data_de_nascimento)
        email = dados.get('email',paciente.email)
        senha = dados.get('senha',paciente.senha_hash)
        


      

        if not isinstance(nome,str): 
            return{'error':'nome invalido'},400
        elif not testa_cpf(cpf):
            return{'error':'cpf invalido'},400
        elif not isinstance(data_de_nascimento,str):
            return{'error':'data_de_nascimento invalido'},400
        elif not testa_email (email):
            return{'error':'email invalido'},400
        
        if  isinstance(senha,str):
            senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())
        else:
            senha_hash = senha


     
       

        paciente.nome = nome
        paciente.cpf = cpf
        paciente.data_de_nascimento = data_de_nascimento
        paciente.email = email
        paciente.senha_hash = senha_hash
       

        db.session.commit()

        return paciente.json(),200



    def delete(self,id):
        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400
        paciente = Paciente.query.get_or_404(id)
        db.session.delete(paciente)
        db.session.commit()
        return paciente.json(),200




class PacienteLogin(MethodView):#/paciente/login
    def post(self):
        """pos(self)-> dict,int
        Faz o sistema de login de um médico"""
        dados = request.json
        email = dados.get("email")
        senha = dados.get("senha")
        if not isinstance(email,str): return {"Erro": "Dado do email não está tipado como String"},400
        if not isinstance(senha,str): return {"Erro": "Dado da senha não está tipado como String"},400
        
        paciente = Paciente.query.filter_by(email=email).first()
        if not paciente or not paciente.verify_senha(senha): 
            return {"Erro":"Email ou Senha Inválidos"},403
        token = create_access_token(identity= paciente.id)
        return {"token":token},200