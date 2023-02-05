from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Usuario, InvestRequests, Tickets

        
@receiver(post_save, sender=Tickets)
def tickets_add_record(sender, instance, **kwargs):
    if instance.rState == "Aprobado" or instance.rState == "Denegado":
        
        InfoUser = Usuario.objects.get(username=instance.username)
        subject = "Solicitud - Abono de Fondos"
        
        if instance.rState == "Aprobado":
            email_template_name = "interface/tickets_email_success.txt"
        
        if instance.rState == "Denegado":
            email_template_name = "interface/tickets_email_deny.txt"

        c = {
        'username': instance.username,
        'tAmmount':instance.tAmmount,
        'tAmmountFrom':instance.tAmmountFrom,
        'tBank':instance.tBank,
        'tBankAccount':instance.tBankAccount,
        'tBankTicket':instance.tBankTicket,        
        'site_name': 'VRT-Fund',
        'protocol': 'https',# http
        'domain':'vrtfund.com',# 127.0.0.1:8000
        }
        email = render_to_string(email_template_name, c)
        
        try:
            send_mail(subject, email, 'noreply@vrtfund.com' , [InfoUser.email], fail_silently=False)
        except Exception as e:
            with open("/home/savelasquezo/apps/vrt/core/logs/email_err.txt", "a") as f:
                f.write("EmailError: {}\n".format(str(e)))


@receiver(post_save, sender=InvestRequests)
def investment_add_record(sender, instance, **kwargs):
    if instance.rState == "Aprobado":
        CUser = Usuario.objects.filter(username=instance.username)
        
        try:
            CUser.update(
                ref_id = instance.staff_cod,
                ref_name = instance.staff,
                ref_interest = 1,
                is_active = True,
                is_operating =True,
                full_name = instance.full_name,
                email = instance.email,
                phone = instance.phone,
                country = instance.country,
                codigo = instance.codigo,
                bank = instance.bank,
                bank_account = instance.bank_account,
                ammount = instance.ammount,
                interest = instance.interest,
                date_expire = instance.date_expire
                )

        except Exception as e:
            with open("/home/savelasquezo/apps/vrt/core/logs/signals.txt", "a") as f:
                f.write("SignalError: {}\n".format(str(e)))

    if instance.rState == "Error":
        CUser = Usuario.objects.filter(username=instance.username)
        
        try:
            CUser.update(is_operating =False)

        except Exception as e:
            with open("/home/savelasquezo/apps/vrt/core/logs/signals.txt", "a") as f:
                f.write("SignalError: {}\n".format(str(e)))
