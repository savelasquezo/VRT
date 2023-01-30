from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Usuario, InvestRequests

@receiver(post_save, sender=InvestRequests)
def add_record(sender, instance, **kwargs):
    if instance.rState == "Aprobado":

        CUser = Usuario.objects.filter(username=instance.username)
        
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
            date_joined = timezone.now(),
            date_expire = instance.date_expire
            )
        
        


        

        
