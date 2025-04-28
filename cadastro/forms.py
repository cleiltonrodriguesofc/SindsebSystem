from .models import Socio, SocioTrabalho, SocioEndereco, SocioDependent
from django import forms

# create forms to get data "socio"
class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = '__all__'

class SocioTrabalhoForm(forms.ModelForm):
    class Meta:
        model = SocioTrabalho
        fields = '__all__'

class SocioEnderecoForm(forms.ModelForm):
    class Meta:
        model = SocioEndereco
        fields = '__all__'

class SocioDependentForm(forms.ModelForm):
    class Meta:
        model = SocioDependent
        fields = '__all__'