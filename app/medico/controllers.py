#controlers

from flask.wrappers import Request
from app.medico.model import Medico
from flask import request,jsonify,render_template
from flask.views import MethodView
#from app.extensions import  email as mail
from app.extensions import db
#from flask_mail import Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils import testa_email, testa_cpf


import bcrypt

class MedicoCreate(MethodView):#'/medico/create'
    

    def get(self):
        medico = Medico.query.all()
        return jsonify ([medico.json()for medico in medico]),200

    def post(self):

        dados = request.json

        nome = dados.get('nome')
        cpf = dados.get('cpf')
        especialidade = dados.get('especialidade')
        email = dados.get('email')
        senha = dados.get('senha')

        #validação de dados
        if not isinstance(nome,str): 
            return{'error':'nome invalido'},400
        elif not testa_cpf(cpf):
            return{'error':'cpf invalido'},400
        elif not isinstance(especialidade,str):
            return{'error':'especialidade invalido'},400
        elif not testa_email (email):
            return{'error':'email invalido'},400
        
        medico = Medico.query.filter_by(email = email).first()

        if medico:
            return {'error':'Email já cadastrado'},400

        medico = Medico.query.filter_by(cpf = cpf).first()

        if medico:
            return {'error':'CPF já cadastrado'},400






        senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())

        medico = Medico(nome=nome,cpf=cpf,especialidade=especialidade,email=email,senha_hash=senha_hash)
        db.session.add(medico)
        db.session.commit()

        #msg = Message(
            #sender= 'julia.xexeo@poli.ufrj.br',
            #recipients=[email],
            #subject= "Cadastro feito com sucesso",
            #html=render_template('email.html',nome=nome)

        #)
        #mail.send(msg)

        return medico.json(),200

class MedicoDetails(MethodView):#'/medico/details/<int:id>'

    decorators = [jwt_required()]
   
    def get (self,id):

        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400
        
        medico = Medico.query.get_or_404(id)
        return medico.json(),200
    
 
    def put (self,id):
        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400

        medico = Medico.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome')
        cpf = dados.get('cpf')
        especialidade = dados.get('especialidade')
        email = dados.get('email')
        senha = dados.get('senha')

       



         #validação de dados
        if not isinstance(nome,str): 
            return{'error':'nome invalido'},400
        elif not  testa_cpf(cpf):
            return{'error':'cpf invalido'},400
        elif not isinstance(especialidade,str):
            return{'error':'especialidade invalido'},400
        elif not testa_email (email):
            return{'error':'email invalido'},400


        senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())
        

        medico.nome = nome
        medico.cpf = cpf
        medico.especialidade = especialidade
        medico.email = email
        medico.senha_hash = senha_hash

        db.session.commit()

        return medico.json(),200
    

    def patch(self,id):

        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400

        medico = Medico.query.get_or_404(id)
        dados = request.json

        nome = dados.get('nome',medico.nome)
        cpf = dados.get('cpf',medico.cpf)
        especialidade = dados.get('especialidade',medico.especialidade)
        email = dados.get('email',medico.email)
        senha = dados.get('senha',medico.senha_hash)
        


      

        if not isinstance(nome,str): 
            return{'error':'nome invalido'},400
        elif not testa_cpf(cpf):
            return{'error':'cpf invalido'},400
        elif not isinstance(especialidade,str):
            return{'error':'especialidade invalido'},400
        elif not testa_email (email):
            return{'error':'email invalido'},400
        
        if  isinstance(senha,str):
            senha_hash = bcrypt.hashpw(senha.encode(),bcrypt.gensalt())
        else:
            senha_hash = senha


     
       

        medico.nome = nome
        medico.cpf = cpf
        medico.especialidade = especialidade
        medico.email = email
        medico.senha_hash = senha_hash
       

        db.session.commit()

        return medico.json(),200



    def delete(self,id):
        if (get_jwt_identity() != id):
            return{'error':'Usuário não permitido '},400
        medico = Medico.query.get_or_404(id)
        db.session.delete(medico)
        db.session.commit()
        return medico.json(),200


class MedicoLogin(MethodView):
    def post(self):
        dados = request.json

           
        email = dados.get('email')
        senha = dados.get('senha')

        medico=Medico.query.filter_by(email = email).first()
        if (not medico) or (not bcrypt.checkpw(senha.encode(), medico.senha_hash)): 
            return{'error':'email ou senha invalidos'},400
        
        token = create_access_token(identity = medico.id)
        return {"token":token},200
