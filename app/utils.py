from re import match

ER_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
ER_numeros = r'^[0-9]{11}$'


def testa_email(email):
  if not isinstance(email,str):
    return False
  if "@" not in email:
    return False
  if not match(ER_email,email):
    return False
  return True




def testa_cpf(cpf):
    if  match(ER_numeros,cpf):
        return True
    return False
    