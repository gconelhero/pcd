import csv

from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.conf import settings

import filetype 
import qrcode

from .forms import LoginForm, CustomUserCreationForm, MemberForm, FilePrescriptionForm, FileReportForm
from .models import Member, MemberCard, FileReport, FilePrescription, user_directory_path

def index(request):
    if request.user.is_authenticated:
        print()
    else:
        print()
    return render(request, 'index.html')

def login_view(request):
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('index')
            else:
                message = 'Usuário ou/e senha inválido(s)'

                return render(request, 'login.html', {'form': form, 'message': message})
    else:
        form = LoginForm()
    
        return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('login'))

def signup_view(request):
    message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
           form.save()

           return HttpResponseRedirect(reverse('login'))
        else:
            message = 'Os dados não foram preenchidos corretamente'
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form, 'message': message})

@login_required
def cadastro_associado(request):
    message = ''
    cadastro, created_ = Member.objects.get_or_create(member=request.user)
    report, created_r = FileReport.objects.get_or_create(report_id=cadastro.member.pk)
    prescription, created_p = FilePrescription.objects.get_or_create(prescription_id=cadastro.member.pk)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=cadastro)
        form_report = FileReportForm(request.POST, request.FILES, instance=report)
        form_prescription = FilePrescriptionForm(request.POST, request.FILES, instance=prescription)
        form.user = request.user
        if request.FILES:
            file_report = request.FILES.get('file_report')
            file_prescription = request.FILES.get('file_prescription')
            try:
                if file_report:
                    file_type_r = filetype.guess(file_report)
                    if file_type_r.MIME != 'application/pdf':
                        message = 'Problema no envio de arquivo.'
                        return render(request, 'cadastro_associado.html', {'form': form, 
                                                                           'form_report': form_report, 
                                                                           'form_prescription': form_prescription,  
                                                                           'message': message})
                if file_prescription:
                    file_type_p = filetype.guess(file_prescription)
                    if file_type_p.MIME != 'application/pdf':
                        message = 'Problema no envio de arquivo.'
                        return render(request, 'cadastro_associado.html', {'form': form, 
                                                                           'form_report': form_report, 
                                                                           'form_prescription': form_prescription,
                                                                           'message': message})
                  
            except:
                message = 'Problema no envio de arquivo.'
                
                return render(request, 'cadastro_associado.html', {'form': form, 
                                                                   'form_report': form_report, 
                                                                   'form_prescription': form_prescription,
                                                                   'message': message})
        

        
        if form.is_valid():
            if form_report.is_valid():                
                form_report.save()
            if form_prescription.is_valid():
                form_prescription.save()
            form.save()

            return HttpResponseRedirect(reverse('associado'))
        else:
            message = 'Os dados não foram preenchidos corretamente'
    else:
        if request.GET.get('state'):
            if not settings.STATIC_ROOT:
                with open(f"{settings.STATIC_URL}municipios/{request.GET.get('state')}.csv", 'r') as cities:
                    cities_list = csv.DictReader(cities)
                    cities_list = [city.split(',')[-1].replace('\n', '') for city in cities]
                    data = {'cities': cities_list}

                return JsonResponse(data, safe=False)    
            with open(f"{settings.STATIC_ROOT}/municipios/{request.GET.get('state')}.csv", 'r') as cities:
                cities_list = csv.DictReader(cities)
                cities_list = [city.split(',')[-1].replace('\n', '') for city in cities]
                data = {'cities': cities_list}

                return JsonResponse(data, safe=False)
        if cadastro:
            form = MemberForm(instance=cadastro)
            form_report = FileReportForm(instance=cadastro)
            form_prescription = FilePrescriptionForm(instance=cadastro)
        else:
            form = MemberForm()
            form_report = FileReportForm()
            form_prescription = FilePrescriptionForm()
    
    return render(request, 'cadastro_associado.html', {'form': form, 
                                                       'form_report': form_report, 
                                                       'form_prescription': form_prescription,
                                                       'message': message})


@login_required
def associado(request):
    message = ''
    file_report = ''
    file_prescription = ''
    member, created_ = Member.objects.get_or_create(member_id=request.user.pk)
    card_flag_template = False
    if not member.state:
        message = 'Para se cadastrar preencha o formulário para associados clicando no botão Cadastro.'
    if member.state and member.city and member.address and member.cid:
            file_report = FileReport.objects.get(report_id=member.member.pk)
            file_prescription = FilePrescription.objects.get(prescription_id=member.member.pk)
            if file_report.file_report:
                card(request)
                card_flag_template = True
    return render(request, 'associado.html', {'message': message, 
                                              'file_report': file_report, 
                                              'file_prescription': file_prescription, 
                                              'card': card_flag_template,  
                                              'member': member})

@login_required
def card(request): 
    message = ''
    member = get_object_or_404(Member, pk=request.user.pk)
    file_report = FileReport.objects.get(report_id=member.member.pk)
    gen_qr = generate_qrcode_data(request, f'{file_report.file_report}')
    qr_code = MemberCard.objects.get(card_id=member.member.pk)
    qr_code_image = f'{qr_code.qr_code_image.url}'
    if request.method == 'POST':
        print(request.POST)

    return render(request, 'card.html', {'member': member, 
                                         'qrcode': qr_code_image, 
                                         'message': message})

def document_view(request):
    message = ''
    member = get_object_or_404(Member, pk=request.user.pk)
    file_report = FileReport.objects.get(report_id=member.member.pk)
    file_prescription = FilePrescription.objects.get(prescription_id=member.member.pk)

    return render(request, 'document_view.html', {'file_reportt': file_report,
                                                  'file_prescription': file_prescription ,
                                                  'message': message, 
                                                  })

def pdf_view(request, *args, **kwargs):
    path_info = request.META['PATH_INFO']
    pdf_path = f"{settings.MEDIA_ROOT}{path_info.split('pdf_view/')[-1]}"
        
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf', as_attachment=False)

@login_required
def generate_qrcode_data(request, pdf_path):
    member = get_object_or_404(Member, pk=request.user.pk)
    card = get_object_or_404(MemberCard, card=member)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
    pdf_url = request.META['HTTP_HOST'] + f'/pdf_view/{pdf_path}' # request.build_absolute_uri(pdf_path) # Utilizar o build_absolute_uri quando tiver a validação dentro desse mesmo view!! (card/)
    qr.add_data(pdf_url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    card.qr_code_data = pdf_url
    user_directory_save = user_directory_path(member, 'qr_image.png')
    card.qr_code_image = user_directory_save
    qr_image.save(f'{settings.MEDIA_ROOT}{card.qr_code_image}')
    card.save()
    
