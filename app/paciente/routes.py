#routes

from app.paciente.model import Paciente
from flask import Blueprint
from app.paciente.controllers import PacienteCreate, PacienteDetails, PacienteLogin

paciente_api = Blueprint('paciente_api',__name__)

paciente_api.add_url_rule(
    '/paciente/create',view_func=PacienteCreate.as_view('paciente_create'),methods=['GET','POST']
)

paciente_api.add_url_rule(
    '/paciente/details/<int:id>',view_func=PacienteDetails.as_view('paciente_details'),methods=['GET','PUT','PATCH','DELETE']
)
paciente_api.add_url_rule(
    '/paciente/login',view_func=PacienteLogin.as_view('paciente_login'),methods=['POST']
)