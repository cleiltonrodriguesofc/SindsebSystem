from .models import Socio, SocioTrabalho, SocioEndereco, SocioDependent
from django import forms

# Form for Socio data
class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = '__all__'

    # Custom validation for email to ensure uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Socio.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

# Form for SocioTrabalho (Work Information)
class SocioTrabalhoForm(forms.ModelForm):
    class Meta:
        model = SocioTrabalho
        fields = '__all__'

# Form for SocioEndereco (Address Information)
class SocioEnderecoForm(forms.ModelForm):
    class Meta:
        model = SocioEndereco
        fields = '__all__'

# Form for SocioDependent (Dependents)
class SocioDependentForm(forms.ModelForm):
    class Meta:
        model = SocioDependent
        fields = '__all__'

    # Custom validation for dependents (optional)
    def clean_dependente(self):
        dependente = self.cleaned_data.get('dependente')
        if dependente and len(dependente.strip()) == 0:
            raise forms.ValidationError("Dependente não pode ser vazio se informado.")
        return dependente
