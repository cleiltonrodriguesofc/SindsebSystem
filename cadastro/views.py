from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Socio, SocioDependent, SocioEndereco, SocioTrabalho, Lotacao



def cadastrar_socio(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip().upper()
        nome = ' '.join(nome.split())

        cargo = request.POST.get('cargo', '').strip().upper()
        cargo = ' '.join(cargo.split())

        lotacao_name = request.POST.get('lotacao', '').strip().upper()
        lotacao_name = ' '.join(lotacao_name.split())

        secretaria = request.POST.get('secretaria', '').strip().upper()
        secretaria = ' '.join(secretaria.split())

        matricula = request.POST.get('matricula', '').strip()
        data_admissao = request.POST.get('data_admissao')
        data_socio = request.POST.get('data_socio')

        rua = request.POST.get('rua', '').strip().upper()
        rua = ' '.join(rua.split())

        numero = request.POST.get('numero', '')  # Ensure it's a string
        numero = numero.strip().upper() if numero else ""

        bairro = request.POST.get('bairro', '').strip().upper()
        bairro = ' '.join(bairro.split())

        uf = request.POST.get('uf', '').strip().upper()
        cidade = request.POST.get('cidade', '').strip().upper()
        cidade = ' '.join(cidade.split())

        cep = request.POST.get('cep', '').strip()
        data_nasc = request.POST.get('data_nasc')

        rg = request.POST.get('rg', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        email = request.POST.get('email', '').strip().lower()

        # Create socio object in model
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

        

        # Create job object and link to socio

        lotacao = Lotacao(
            socio=socio,
            socio_lotacao=lotacao_name,  
            secretaria=secretaria,
        )
        lotacao.save()
        
        trabalho = SocioTrabalho(
            socio=socio,  # Linking it to socio
            cargo=cargo,
            data_admissao=data_admissao,
            lotacao=lotacao
        )
        trabalho.save()

        

        # Create address object and link to socio
        endereco = SocioEndereco(
            socio=socio,  # Linking it to socio
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            cep=cep,
            uf=uf
        )
        endereco.save()

        # Get dependents names dynamically
        for i in range(1, 5):
            nome_dependente = request.POST.get(f'dependente{i}', '').strip().upper()
            nome_dependente = ' '.join(nome_dependente.split())

            if nome_dependente:  # Only create if there's a valid name
                dependente = SocioDependent(
                    socio=socio,  # Linking to socio
                    nome=nome_dependente
                )
                dependente.save()

        return render(request, 'cadastro/cadastrar.html')
    else:
        return render(request, 'cadastro/cadastrar.html')
