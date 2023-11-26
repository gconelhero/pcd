import hashlib
import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import qrcode

from pcd.settings import MEDIA_ROOT
from .managers import CustomUserManager

def user_directory_path(instance, filename):
    ext = filename[-4:]
    user_id_bytes = str(instance.id).encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(user_id_bytes)
    new_filename = sha256.hexdigest()
    if filename[:-4] == 'report':
        filename = f'{new_filename[:5]}_report{ext}'
        instance.upload_report_date = timezone.now()
    elif filename[:-4] == 'prescription':
        instance.upload_prescription_date = timezone.now()
        filename = f'{new_filename[:5]}_prescription{ext}'
    elif filename[:-4] == 'qr_image':
        filename = f'{new_filename[:5]}_qrcode{ext}'
    else:
        filename = f'{new_filename[:5]}{ext}'
    file_path = f"{instance.id}/"
    try:
        if filename in os.listdir(f'{MEDIA_ROOT}{file_path}'):
            os.remove(f'{MEDIA_ROOT}{file_path}{filename}')
    except:
        return f"{file_path}{filename}"
    
    return f"{file_path}{filename}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), unique=True)
    name = models.CharField(_("name"), max_length=30, blank=False)
    last_name = models.CharField(_("last_name"), max_length=50, blank=False)
    birthday = models.DateField(_("birthday") ,null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=15, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # verificação por email
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Member(models.Model):
    member = models.OneToOneField("CustomUser", on_delete=models.CASCADE, related_name="member")
    state = models.CharField(max_length=3, blank=False)
    city = models.CharField(max_length=100, blank=False)
    address = models.CharField(_("address"), max_length=50, blank=False)
    cid = models.CharField(_("cid"), max_length=15, blank=False)
    responsavel = models.BooleanField(_("responsavel"), default=False)
    nome_responsavel = models.CharField(_("nome_responsavel"), max_length=100, blank=True, null=True)
    alergia = models.CharField(_("alergia"), max_length=255, blank=True, null=True)
    sensibilidade = models.CharField(_("sensibilidade"), max_length=255, blank=True, null=True)
    profile_image = models.ImageField(_("profile image"), upload_to=user_directory_path)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True) # date_create change var name
    #number
    #cep

    def __str__(self):
        return self.member.email

    def save(self, *args, **kwargs):
        MemberCard.objects.get_or_create(card_id=self.member.pk) # para replace de qrcode quando documentos atualizados
        if self.responsavel == False:
            self.nome_responsavel = None
        super().save(*args, **kwargs)

class FileReport(models.Model):
    report = models.OneToOneField("Member", on_delete=models.CASCADE, related_name="report")
    file_report = models.FileField(_("document report"), upload_to=user_directory_path, blank= True, null=True) # Terminar de configurar a entrada dos arquivos no model
    upload_report_date = models.DateTimeField(blank=True, null=True) # or default=timezone.now

    def __str__(self):
        return self.file_report.name

    def save(self, *args, **kwargs):
        if not self.file_report:
            self.upload_report_date = None
        elif self.file_report:
            self.file_report.name = 'report.pdf'
            self.upload_report_date = timezone.now()
        super().save(*args, **kwargs)
        
class FilePrescription(models.Model):
    prescription = models.OneToOneField("Member", on_delete=models.CASCADE, related_name="prescription")
    file_prescription = models.FileField(_("document prescription"), upload_to=user_directory_path, blank= True, null=True)
    upload_prescription_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.file_prescription.name

    def save(self, *args, **kwargs):
        if not self.file_prescription:
            self.upload_prescription_date = None
        elif self.file_prescription:
            self.file_prescription.name = 'prescription.pdf'
        super().save(*args, **kwargs)

# criar uma lógica para tempo de validade do cartão
class MemberCard(models.Model):
    card = models.OneToOneField("Member", on_delete=models.CASCADE, related_name="card")
    qr_code_data = models.CharField(_("qr code data"), max_length=255, blank=True, null=True)
    qr_code_image = models.ImageField(_("qr code image"), upload_to=user_directory_path)
    is_active = models.BooleanField(default=True) # Fazer a lógica posterior
    gen_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.card}'

    def save(self, *args, **kwargs):
        self.gen_date = timezone.now()
        super().save(*args, **kwargs)
