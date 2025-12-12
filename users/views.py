# users/views.py (Código Corrigido)

from django.shortcuts import render, redirect # Importar redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from datetime import datetime

# Models
from users.models import AccountRequest

db_name = 'appDB'

def login(request):
    return render(request, 'login.html')

def request(request):
    if request.method == "GET":
        return render(request, 'request.html')
    else:
        # Se for POST, processa os dados
        FULLNAME = request.POST.get('req_fullname')
        EMAIL = request.POST.get('req_email')
        PASSWORD = request.POST.get('req_password')
        COMPANY_NAME = request.POST.get('req_client_name')

        # VALIDAÇÃO: SELECT no Banco de Dados (Verificar se o email já existe)
        try:
            if AccountRequest.objects.using(db_name).filter(EMAIL=EMAIL).exists():
                # E-mail já possui uma solicitação na fila (Caminho 1 - OK)
                context = {'error': 'Este e-mail já possui uma solicitação de conta pendente ou em análise. Por favor, aguarde.'}
                return render(request, 'request.html', context)
        
        except Exception as e:
            # Caso haja um erro de conexão ou de DB (Caminho 2 - OK)
            print(f"Erro ao consultar o banco de dados externo ({db_name}): {e}")
            context = {'error': 'Ocorreu um erro interno ao verificar a conta. Tente novamente mais tarde.'}
            return render(request, 'request.html', context)
        
        hashed_password = make_password(PASSWORD)
        
        # 2. Criar e Salvar o novo objeto AccountRequest
        new_request = AccountRequest.objects.using(db_name).create(
            FULLNAME=FULLNAME,
            EMAIL=EMAIL,
            PASSWORD=hashed_password,
            COMPANY_NAME=COMPANY_NAME,
            REQ_DATE = datetime.now(),
            STATUS = "Pending"
        )
        return redirect('login')