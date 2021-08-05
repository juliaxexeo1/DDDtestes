#routes

from app.medico.model import Medico
from flask import Blueprint
from app.medico.controllers import MedicoCreate, MedicoDetails, MedicoLogin

medico_api = Blueprint('medico_api',__name__)

medico_api.add_url_rule(
    '/medico/create',view_func=MedicoCreate.as_view('medico_create'),methods=['GET','POST']
)

medico_api.add_url_rule(
    '/medico/details/<int:id>',view_func=MedicoDetails.as_view('medicos_details'),methods=['GET','PUT','PATCH','DELETE']
)
medico_api.add_url_rule(
    '/medico/login',view_func=MedicoLogin.as_view('medico_login'),methods=['POST']
)