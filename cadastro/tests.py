from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import Socio

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
