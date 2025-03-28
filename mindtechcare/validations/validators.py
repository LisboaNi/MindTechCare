from django.contrib.auth.hashers import make_password
import re

def encrypt_password(password):
    return make_password(password)

def validate_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False

    # CNPJs inválidos (sequências repetidas como "00000000000000", "11111111111111", etc.)
    if cnpj == cnpj[0] * 14:
        return False

    # Calcula os dois dígitos verificadores
    def calcular_digito_verificador(cnpj, posicoes):
        soma = 0
        for i in range(len(posicoes)):
            soma += int(cnpj[i]) * posicoes[i]
        digito = 11 - (soma % 11)
        return digito if digito < 10 else 0

    # Cálculo do primeiro dígito verificador
    posicoes_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    primeiro_digito = calcular_digito_verificador(cnpj, posicoes_1)

    # Cálculo do segundo dígito verificador
    posicoes_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    segundo_digito = calcular_digito_verificador(cnpj, posicoes_2)

    # Verifica se os dígitos calculados são iguais aos dígitos fornecidos
    if int(cnpj[12]) == primeiro_digito and int(cnpj[13]) == segundo_digito:
        return True
    else:
        return False