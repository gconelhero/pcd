from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from .models import CustomUser, Member, FileReport, FilePrescription

ESTADOS = (('',''),('AC','Acre AC'),('AL','Alagoas AL'),('AP','Amapá AP'),
            ('AM','Amazonas AM'),('BA','Bahia BA'),('CE','Ceará CE'),
            ('DF','Distrito Federal DF'),('ES','Espírito Santo ES'),
            ('GO','Goiás GO'),('MA','Maranhão MA'),('MT','Mato Grosso MT'),
            ('MS','Mato Grosso do Sul MS'),('MG','Minas Gerais MG'),('PA','Pará PA'),
            ('PB','Paraíba PB'),('PR','Paraná PR'),('PE','Pernambuco PE'),('PI','Piauí PI'),
            ('RJ','Rio de Janeiro RJ'),('RN','Rio Grande do Norte RN'),
            ('RS','Rio Grande do Sul RS'),('RO','Rondônia RO'),('RR','Roraima RR'),
            ('SC','Santa Catarina SC'),('SP','São Paulo SP'),('SE','Sergipe SE'),
            ('TO','Tocantins TO'))


class LoginForm(forms.Form):
    username = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    last_name = forms.CharField(label='Sobrenome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}))
    email = forms.CharField(label='E-Mail', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Telefone', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', }))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('name', 
                  'last_name',
                  'email',
                  'birthday',
                  'phone',
                  'password1',
                  'password2',
                  )


class CustomUserChangeForm(UserChangeForm):
    name = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    last_name = forms.CharField(label='Sobrenome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}))
    email = forms.CharField(label='E-Mail', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Telefone', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', }))
    
    class Meta:
        model = CustomUser
        fields = ('name', 
                  'last_name', 
                  'email', 
                  'birthday', 
                  'phone', 
                  )


class MemberForm(forms.ModelForm):
    state = forms.ChoiceField(label='UF', choices=ESTADOS, widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.ChoiceField(label='Município', widget=forms.Select(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Endereço', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}))
    cid = forms.CharField(label='CID', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CID-10 F...'}))
    alergia = forms.CharField(label='Alergia', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva'}))
    sensibilidade = forms.CharField(label='Sensibilidade', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descreva'}))
    responsavel = forms.BooleanField(label='Responsável', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control form-check-input', 
                                                                                                           'placeholder': 'Endereço', }))
    nome_responsavel = forms.CharField(label='Nome do responsável', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 
                                                                                                                  'placeholder': 'Nome completo do responsável'}))
    class Meta:
        model = Member
        fields = ('state', 
                  'city',
                  'address', 
                  'cid', 
                  'alergia', 
                  'sensibilidade', 
                  'responsavel', 
                  'nome_responsavel', 
                  )

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices = self.get_dynamic_choices()
        
    def get_dynamic_choices(self):
        selected_state = self['state'].value()
        if selected_state:
            with open(f"{settings.STATIC_ROOT}/municipios/{selected_state}.csv") as cities: # Configurar posterio para deploy
                cities_list = [(city.split(',')[-1].replace('\n', ''), city.split(',')[-1].replace('\n', '')) for city in cities]

            return cities_list
        return []

class FileReportForm(forms.ModelForm):
    file_report = forms.FileField(label='Laudo', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = FileReport
        fields = ('file_report',)

class FilePrescriptionForm(forms.ModelForm):
    file_prescription = forms.FileField(label='Receita', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = FilePrescription
        fields = ('file_prescription',)
