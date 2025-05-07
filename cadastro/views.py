from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from .models import Socio, SocioDependent, SocioEndereco, SocioTrabalho, Lotacao
from django.contrib import messages


def clean_str(value):
    """Clean string by stripping, converting to uppercase, and removing extra spaces."""
    return ' '.join(value.strip().upper().split()) if value else ''

def cadastrar_socio(request):
    # List of states processed before passing to the template
    states = "AC,AL,AP,AM,BA,CE,DF,ES,GO,MA,MT,MS,MG,PA,PB,PR,PE,PI,RJ,RN,RS,RO,RR,SC,SP,SE,TO"
    state_list = states.split(',')

    if request.method == 'POST':
        nome = clean_str(request.POST.get('nome'))
        if not nome:
            return render(request, 'cadastro/cadastrar.html', {
                'error': 'Este campo é obrigatório',
                'state_list': state_list
            }
        )

        cargo = clean_str(request.POST.get('cargo'))
        lotacao_name = clean_str(request.POST.get('lotacao'))
        secretaria = clean_str(request.POST.get('secretaria'))

        matricula = request.POST.get('matricula', '').strip()
        data_admissao = request.POST.get('data_admissao')
        data_socio = request.POST.get('data_socio')
        data_nasc = request.POST.get('data_nasc')
        if data_nasc:
            born = date.fromisoformat(data_nasc)
            today = date.today()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day)) 
            if age < 18:
                messages.error(request, "O sócio deve ter pelo menos 18 anos.")
                return render(request, 'cadastro/cadastrar.html', {'form_data': request.POST})

        rua = clean_str(request.POST.get('rua'))
        numero = request.POST.get('numero', '').strip().upper() if request.POST.get('numero') else ''
        bairro = clean_str(request.POST.get('bairro'))
        cidade = clean_str(request.POST.get('cidade'))
        uf = clean_str(request.POST.get('uf'))
        cep = request.POST.get('cep', '').strip()

        rg = request.POST.get('rg', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        email = request.POST.get('email', '').strip().lower()

        # Create and save Socio
        socio = Socio(
            matricula=matricula,
            nome=nome,
            data_nasc=data_nasc,
            cpf=cpf,
            rg=rg,
            telefone=telefone,
            data_socio=data_socio,
            email=email
        )
        socio.save()

        # Get or create Lotacao
        lotacao, _ = Lotacao.objects.get_or_create(
            socio=socio,
            socio_lotacao=lotacao_name,
            secretaria=secretaria
        )

        # Create SocioTrabalho
        trabalho = SocioTrabalho(
            socio=socio,
            cargo=cargo,
            data_admissao=data_admissao,
            lotacao=lotacao
        )
        trabalho.save()

        # Create SocioEndereco
        endereco = SocioEndereco(
            socio=socio,
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            cep=cep,
            uf=uf
        )
        endereco.save()

        # Create SocioDependent entries (up to 4)
        for i in range(1, 5):
            nome_dependente = clean_str(request.POST.get(f'dependente{i}', ''))
            if nome_dependente:
                dependente = SocioDependent(socio=socio, nome=nome_dependente)
                dependente.save()

        # Return to the same page with a success message
        return render(request, 'cadastro/cadastrar.html', {'success': 'Sócio cadastrado com sucesso!', 'state_list': state_list})

    else:
        # Initial page load, pass the state list to the template
        return render(request, 'cadastro/cadastrar.html', {'state_list': state_list})
