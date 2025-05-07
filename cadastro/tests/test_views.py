from django.test import TestCase
from cadastro.models import Socio
from django.urls import reverse


class CadastroSocioViewTest(TestCase):
    def test_form_submission_registers_socio(self):
        # Simulate form data
        form_data = {
            'nome': 'Cleilton Teste',
            'cargo': 'Analista',
            'lotacao': 'Prefeitura',
            'secretaria': 'Financeiro',
            'matricula': '123456',
            'data_admissao': '2024-01-01',
            'data_socio': '2024-04-01',
            'rua': 'Rua A',
            'numero': '100',
            'bairro': 'Centro',
            'uf': 'MA',
            'cidade': 'Buriticupu',
            'cep': '65393000',
            'data_nasc': '1996-06-10',
            'rg': '1234567',
            'cpf': '123.456.789-00',
            'telefone': '999999999',
            'email': 'cleilton@example.com',
            # Dependents (optional)
            'dependente1': 'Filho 1',
            'dependente2': '',
            'dependente3': '',
            'dependente4': '',
        }

        # POST to your view
        response = self.client.post('/cadastro/cadastrar_socio/', form_data)

        # Check if the Socio was created
        self.assertEqual(Socio.objects.count(), 1)
        
        socio = Socio.objects.first()
        self.assertEqual(socio.nome, 'CLEILTON TESTE')  # Should be uppercased as your view does

        # Check if the page rendered (status code 200)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro/cadastrar.html')



    def test_missing_nome_field_does_not_create_socio(self):
        form_data = {
            # 'nome' is intentionally missing
            'cargo': 'Analista',
            'lotacao': 'Prefeitura',
            'secretaria': 'Financeiro',
            'matricula': '123456',
            'data_admissao': '2024-01-01',
            'data_socio': '2024-04-01',
            'rua': 'Rua A',
            'numero': '100',
            'bairro': 'Centro',
            'uf': 'MA',
            'cidade': 'Buriticupu',
            'cep': '65393000',
            'data_nasc': '2025-06-10',
            'rg': '1234567',
            'cpf': '123.456.789-00',
            'telefone': '999999999',
            'email': 'cleilton@example.com',
        }

        response = self.client.post('/cadastro/cadastrar_socio/', form_data)

        self.assertEqual(Socio.objects.count(), 0)
        self.assertEqual(response.status_code, 200)  # The form is re-rendered
        self.assertContains(response, "Este campo é obrigatório")  # Django default error
    
    
    def test_socio_with_underage_date_of_birth_is_not_created(self):
        # Data de nascimento que gera idade menor que 18 anos
        form_data = {
            'nome': 'Menor de Idade',
            'cargo': 'Estagiário',
            'lotacao': 'Secretaria de Juventude',
            'secretaria': 'Juventude',
            'matricula': '999999',
            'data_admissao': '2024-01-01',
            'data_socio': '2024-04-01',
            'rua': 'Rua Jovem',
            'numero': '200',
            'bairro': 'Nova Era',
            'uf': 'MA',
            'cidade': 'Buriticupu',
            'cep': '65393000',
            'data_nasc': '2010-01-01',  # Menor de idade
            'rg': '9876543',
            'cpf': '987.654.321-00',
            'telefone': '988888888',
            'email': 'menor@example.com',
        }

        response = self.client.post('/cadastro/cadastrar_socio/', form_data)

        self.assertEqual(Socio.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "O sócio deve ter pelo menos 18 anos")  # Mensagem personalizada