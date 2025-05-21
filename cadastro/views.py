from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from .models import Socio, SocioDependent, SocioEndereco, SocioTrabalho, Lotacao
from django.contrib import messages
from .forms import SocioForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/cadastro/dashboard/'})
        else:
            return JsonResponse({'success': False, 'error': 'E-mail ou senha inválidos.'}, status=401)

    return render(request, 'cadastro/login.html')


def logout_view(request):
    logout(request)
    return redirect('website:index')


@login_required(login_url='/login/')
def dashboard(request):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Bem-vindo ao dashboard, autenticado!'})
    
    total_socios = Socio.objects.count()
    ativos = Socio.objects.filter(data_socio__isnull=False).count()
    inativos = total_socios - ativos
    documentos_vencendo = 25  # Placeholder, you can replace with actual logic

    # Get the 10 most recent socios
    recent_socios = Socio.objects.order_by('-data_socio')[:10]

    context = {
        "total_socios": total_socios,
        "ativos": ativos,
        "inativos": inativos,
        "documentos_vencendo": documentos_vencendo,
        "recent_socios": recent_socios
    }

    return render(request, 'cadastro/dashboard.html', context)


def editar_socio(request, socio_id):
    socio = get_object_or_404(Socio, pk=socio_id)

    states = "AC,AL,AP,AM,BA,CE,DF,ES,GO,MA,MT,MS,MG,PA,PB,PR,PE,PI,RJ,RN,RS,RO,RR,SC,SP,SE,TO"
    state_list = states.split(',')

    if request.method == 'POST':
        nome = clean_str(request.POST.get('nome'))
        if not nome:
            messages.error(request, 'O nome é obrigatório.')
            return render(request, 'cadastro/editar_socio.html', {
                'socio': socio,
                'state_list': state_list
            })

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
                return render(request, 'cadastro/editar_socio.html', {
                    'socio': socio,
                    'state_list': state_list
                })

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

        # Atualiza Socio
        socio.nome = nome
        socio.matricula = matricula
        socio.data_nasc = data_nasc or None
        socio.cpf = cpf
        socio.rg = rg
        socio.telefone = telefone
        socio.email = email
        socio.data_socio = data_socio or None
        socio.save()

        # Atualiza ou cria Lotacao
        lotacao, _ = Lotacao.objects.get_or_create(
            socio=socio,
            socio_lotacao=lotacao_name,
            secretaria=secretaria
        )

        # Atualiza ou cria SocioTrabalho
        SocioTrabalho.objects.update_or_create(
            socio=socio,
            defaults={
                'cargo': cargo,
                'data_admissao': data_admissao or None,
                'lotacao': lotacao
            }
        )

        # Atualiza ou cria SocioEndereco
        SocioEndereco.objects.update_or_create(
            socio=socio,
            defaults={
                'rua': rua,
                'numero': numero,
                'bairro': bairro,
                'cidade': cidade,
                'uf': uf,
                'cep': cep
            }
        )

        # Atualiza dependentes
        SocioDependent.objects.filter(socio=socio).delete()
        for i in range(1, 5):
            nome_dependente = clean_str(request.POST.get(f'dependente{i}', ''))
            if nome_dependente:
                SocioDependent.objects.create(socio=socio, nome=nome_dependente)

        messages.success(request, "Sócio atualizado com sucesso!")
        return redirect('cadastro:ver_socio', socio_id=socio.id)

    # GET
    try:
        trabalho = SocioTrabalho.objects.get(socio=socio)
    except SocioTrabalho.DoesNotExist:
        trabalho = None

    try:
        endereco = SocioEndereco.objects.get(socio=socio)
    except SocioEndereco.DoesNotExist:
        endereco = None

    dependentes = list(SocioDependent.objects.filter(socio=socio))
    while len(dependentes) < 4:
        dependentes.append(None)

    return render(request, 'cadastro/editar_socio.html', {
        'socio': socio,
        'trabalho': trabalho,
        'endereco': endereco,
        'dependentes': dependentes,
        'state_list': state_list
    })



def ver_socio(request, socio_id):
    socio = get_object_or_404(Socio, pk=socio_id)
    try:
        trabalho = SocioTrabalho.objects.get(socio=socio)
        endereco = SocioEndereco.objects.get(socio=socio)
        lotacao = trabalho.lotacao if trabalho else None
    except:
        trabalho = endereco = lotacao = None

    return render(request, 'cadastro/ver_socio.html', {
        'socio': socio,
        'trabalho': trabalho,
        'endereco': endereco,
        'lotacao': lotacao,
    })

def listar_socios(request):
    socios = Socio.objects.all()
    lista_socios = []

    for socio in socios:
        try:
            trabalho = SocioTrabalho.objects.get(socio=socio)
            lotacao = trabalho.lotacao
            local_trabalho = lotacao.socio_lotacao
            secretaria = lotacao.secretaria if lotacao else ''
        except SocioTrabalho.DoesNotExist:
            local_trabalho = ''
            secretaria = ''

        lista_socios.append({
            'id': socio.id,
            'matricula': socio.matricula,
            'nome': socio.nome,
            'cpf': socio.cpf,
            'local_trabalho': local_trabalho,
            'secretaria': secretaria,
        })

    return render(request, 'cadastro/listar_socios.html', {
        'socios': lista_socios,
    })



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
