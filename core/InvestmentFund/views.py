import os
import re

from openpyxl import Workbook
from openpyxl import load_workbook

from datetime import datetime, timedelta

from django.utils import timezone
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView

from .tools import gToken

from .models import Usuario, Tickets, InvestRequests, FEE

class HomeView(TemplateView):
    template_name='home/home.html'


class SingupView(UserPassesTestMixin, TemplateView):
    template_name='registration/singup.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse('Home'))

    def post(self, request, *args, **kwargs):
        
        iUsername = request.POST['username']
        iPass = request.POST['password']
        iFullName = request.POST['name']
        iEmail = request.POST['email']

        LastID = Usuario.objects.latest('id').id + 1

        if not re.match(r'^[a-zA-Z0-9]+$', iUsername):
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, f'El Nombre de Usuario no es Valido', extra_tags="info") 
            return redirect(reverse('Singup'))

        if Usuario.objects.filter(username=iUsername):
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, f'El Nombre de Usuario no esta Disponible', extra_tags="info") 
            return redirect(reverse('Singup'))

        if Usuario.objects.filter(email=iEmail):
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, f'El Email no esta Disponible', extra_tags="info") 
            return redirect(reverse('Singup'))
        
        
        request.session['django_messages'] = []

        try:
            nUser = Usuario.objects.create(
                username = iUsername,
                full_name = iFullName,
                email = iEmail,
                codigo = LastID
            )
            
            nUser.set_password(iPass)
            nUser.save()

            #login(request, nUser)
            
            messages.success(request, '¡Registro Exitoso!', extra_tags="title")
            messages.success(request, f'Hemos enviado un Email para verificar su cuenta', extra_tags="info")
            
            try:
                cUser = Usuario.objects.get(username=iUsername)
                
                subject = "Activacion - VRTFund"
                email_template_name = "registration/email_confirm.txt"
                c = {
                'username': iUsername,
                "uid": urlsafe_base64_encode(force_bytes(cUser.pk)),
                "user": cUser,
                'token': gToken.make_token(cUser),
                'site_name': 'VRT-Fund',
                'protocol': 'https',# http
                'domain':'vrtfund.com',# 127.0.0.1:8000
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'noreply@vrtfund.com' , [iEmail], fail_silently=False)
                except BadHeaderError:
                    with open("/home/savelasquezo/apps/vrt/core/logs/email_err.txt", "a") as f:
                        eDate = timezone.now().strftime("%Y-%m-%d %H:%M")
                        f.write("EmailError SingupEmail--> {} Error: {}\n".format(eDate, str(e)))
                    return HttpResponse('Invalid Header Found')
                
            except Exception as e:
                with open("/home/savelasquezo/apps/vrt/core/logs/email_err.txt", "a") as f:
                    eDate = timezone.now().strftime("%Y-%m-%d %H:%M")
                    f.write("EmailError SingupConfig--> {} Error: {}\n".format(eDate, str(e)))

        except Exception as e:
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, f'Ha ocurrido un error durante el registro', extra_tags="info")         
        
        return redirect(reverse('Singup'))

class UserLoginView(UserPassesTestMixin, LoginView):
    template_name='registration/login.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse('Home'))

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario/Contraseña Incorrectos', extra_tags="title")
        messages.error(self.request, 'Intentelo Nuevamente', extra_tags="info")
        return super().form_invalid(form)


class InvestmentView(LoginRequiredMixin, TemplateView):
    template_name='home/investment.html'
   
class InfoFormView(LoginRequiredMixin, TemplateView):
    template_name='home/info_ticket.html'

class InfoView(LoginRequiredMixin, TemplateView):
    template_name='home/info.html'
    
    def post(self, request, *args, **kwargs):
        
        InfoUser = Usuario.objects.get(id=request.user.id)
        iUsername = InfoUser.username

        if InfoUser.is_operating:
            messages.error(request, 'ERROR', extra_tags="title")
            messages.error(request, 'Actualmente ya cuenta con una Inversión Activa', extra_tags="info")
            return redirect(reverse('Info')) 

        rInstanceUser = Usuario.objects.get(username=iUsername)
        
        try:
            iCode = InvestRequests.objects.last().pk
        except TypeError:
            iCode = 0
        
        iName = InfoUser.full_name
        iEmail = InfoUser.email
        iCountry = request.POST['country']
        iPhone = request.POST['phone']
        iAmmount = int(request.POST['ammount'])

        iBank = str(request.POST['bank'])
        iBankAccount = request.POST['bank_account']
        iCommentText = request.POST['comment_text']
        
        rtimedelta = request.POST['rtimedelta']
    
        if rtimedelta == "m1":
            Interest = 1
            iDateExpire = timezone.now() + timedelta(days=90)
            
        if rtimedelta == "m2":
            Interest = 2
            iDateExpire = timezone.now() + timedelta(days=180)
            
        if rtimedelta == "m3":
            Interest = 3
            iDateExpire = timezone.now() + timedelta(days=365)

        iDateString = iDateExpire.isoformat()
        iDateObject = datetime.fromisoformat(iDateString) 

        try:
            InvestRequests.objects.create(
                username = rInstanceUser,
                codigo = iCode,
                full_name = iName,
                email = iEmail,
                country = iCountry,
                phone = iPhone,
                ammount = iAmmount,
                bank = iBank,
                bank_account = iBankAccount,
                CommentText = iCommentText,
                staff = "Anonimo",
                staff_cod = 0,
                date_joined = timezone.now(),
                interest = Interest,
                date_expire = iDateObject,
                rState = "Pendiente"
                ) 

            subject = "Solicitud - Información Inversión"        
            email_template_name = "home/info_email.txt"

            c = {
            'tU': iUsername,
            'tName':iName,
            'tAmmountFrom':iAmmount,
            'tBank':iBank,   
            'site_name': 'VRT-Fund',
            'protocol': 'https',# http
            'domain':'vrtfund.com',# 127.0.0.1:8000
            }
            email = render_to_string(email_template_name, c)

            try:
                send_mail(subject, email, 'noreply@vrtfund.com' , [email], fail_silently=False)
            except Exception as e:
                with open("/home/savelasquezo/apps/vrt/core/logs/email_err.txt", "a") as f:
                    eDate = timezone.now().strftime("%Y-%m-%d %H:%M")
                    f.write("EmailError InfoEmail--> {} Error: {}\n".format(eDate, str(e)))
            
            messages.success(request, 'Solicitud Registrada', extra_tags="title")
            messages.success(request, f'Hemos enviado un correo con información del proceso de Inscripción', extra_tags="info")
            return redirect(reverse('Info'))

        except Exception as e:
            with open("/home/savelasquezo/apps/vrt/core/logs/log_err.txt", "a") as f:
                eDate = timezone.now().strftime("%Y-%m-%d %H:%M")
                f.write("QueryError InfoForm--> {} Error: {}\n".format(eDate, str(e)))
            
            messages.error(request, 'ERROR', extra_tags="title")
            messages.error(request, 'La solicitud no se ha podido procesar', extra_tags="info")
            return redirect(reverse('Info')) 

#LoginRequiredMixin
class ContentView(TemplateView):
    template_name='home/content.html'
    

#LoginRequiredMixin
class BenefitView(TemplateView):
    template_name='home/benefit.html'
    

class InterfaceView(LoginRequiredMixin, TemplateView):
    template_name='interface/interface.html'
    

class LegalView(LoginRequiredMixin, TemplateView):
    template_name='home/legal.html'
        

class TicketFormView(LoginRequiredMixin, TemplateView):
    template_name='interface/tickets.html'
    

class HistoryListView(LoginRequiredMixin, TemplateView):
      
    template_name='interface/history.html'

    def days_until_next_month(self):
        Today = timezone.now()
        NextMonth = Today.replace(day=28) + timedelta(days=4)
        TimeDelta = NextMonth.replace(day=1) - Today
        return TimeDelta.days

    def get(self, request, *args, **kwargs):
        
        ITEMS = 5
        MAXPAGES = 5
        
        OTickets = Tickets.objects.filter(username=request.user.id).order_by("-date")[:ITEMS*MAXPAGES]
        ListTicketsPages = Paginator(OTickets,ITEMS).get_page(request.GET.get('page'))
        
        TicketsFix = ITEMS - len(OTickets)%ITEMS
        
        if TicketsFix == ITEMS and len(OTickets) != 0:
            TicketsFix = 0
        
        context = self.get_context_data(**kwargs)
        context={
            'ListTicketsPages':ListTicketsPages,
            'FixTicketsPage':range(0,TicketsFix)
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        InfoUser = Usuario.objects.get(id=request.user.id)
        AviableTickets = InfoUser.available_tickets
        
        rAmmount = int(request.POST['ammount'])
        rAmmountFrom = request.POST['ammount_from']
        rBank = request.POST['bank']
        rBankAccount = request.POST['bank_account']
        rComment = request.POST["message"]
        rState = "Pendiente"
        
        if AviableTickets < 1:
            messages.error(request, 'ERROR', extra_tags="title")
            messages.error(request, '¡Ha excedido el número de retiros Mensuales!', extra_tags="info")
            return redirect(reverse('History'))

        if rAmmountFrom == "f1":
            rAmmountFrom = "Intereses"
            
            if rAmmount > InfoUser.available:
                messages.error(request, 'ERROR', extra_tags="title")
                messages.error(request, 'La solicitud no se ha podido procesar', extra_tags="info")
                return redirect(reverse('History'))
            
            Usuario.objects.filter(id=InfoUser.id).update(
                available=F('available')-rAmmount,
                paid=F('paid')+rAmmount
                )

        if rAmmountFrom == "f2":
            rAmmountFrom = "Comisiones"
            
            if rAmmount > InfoUser.ref_available:
                messages.error(request, 'ERROR', extra_tags="title")
                messages.error(request, 'La solicitud no se ha podido procesar', extra_tags="info")
                return redirect(reverse('History'))
            
            Usuario.objects.filter(id=InfoUser.id).update(
                ref_available=F('ref_available')-rAmmount,
                ref_paid=F('ref_paid')+rAmmount
                )

        if rAmmountFrom == "f3":
            rAmmountFrom = "Mixto"
            rPaidAvailable= int(InfoUser.available)
            rPaidRef = int(InfoUser.ref_available)
            
            Total = rPaidAvailable + rPaidRef
            if rAmmount > Total:
                messages.error(request, 'ERROR', extra_tags="title")
                messages.error(request, 'La solicitud no se ha podido procesar', extra_tags="info")
                return redirect(reverse('History'))

    
            Usuario.objects.filter(id=InfoUser.id).update(
                available=0,
                paid=F('paid')+rPaidAvailable,
                ref_available=0,
                ref_paid=F('ref_paid')+rPaidRef
                )

        rAmmountFee = rAmmount - FEE
        
        Tickets.objects.create(
            username = InfoUser,
            tAmmount = rAmmountFee,
            tAmmountFrom = rAmmountFrom,
            tBank= rBank,
            tBankAccount = rBankAccount,
            CommentText = rComment,
            rState=rState
            ) 

        TimeDelta = self.days_until_next_month()

        InfoUser = Usuario.objects.get(id=request.user.id)
        AviableTickets = InfoUser.available_tickets

        subject = "Notificación - Solicitud de Retiro"        
        email_template_name = "interface/tickets_email_notify.txt"

        c = {
        'username': InfoUser.username,
        'tAmmount':rAmmount,
        'tAmmountFrom':rAmmountFrom,
        'tBank':rBank,
        'tBankAccount':rBankAccount,   
        'TimeDelta':TimeDelta,    
        'site_name': 'VRT-Fund',
        'protocol': 'https',# http
        'domain':'vrtfund.com',# 127.0.0.1:8000
        }
        email = render_to_string(email_template_name, c)

        try:
            send_mail(subject, email, 'noreply@vrtfund.com' , [InfoUser.email], fail_silently=False)
        except Exception as e:
            with open("/home/savelasquezo/apps/vrt/core/logs/email_err.txt", "a") as f:
                eDate = timezone.now().strftime("%Y-%m-%d %H:%M")
                f.write("EmailTicket Notification--> {} Error: {}\n".format(eDate, str(e)))


        FileName = '/home/savelasquezo/apps/vrt/core/logs/users/'+ InfoUser.username + '.xlsx'

        if not os.path.exists(FileName):
            WB = Workbook()
            WS = WB.active
            WS.append(["Tipo","Fecha", "$Interes", "$Comiciones", "AcInteres", "AcComisiones", "$Ticket", "Origen", "Total"])
        else:
            WB = load_workbook(FileName)
            WS = WB.active

        NowToday = timezone.now().strftime("%Y-%m-%d %H:%M")

        FileData = [0, NowToday, "", "", "", "", rAmmount, rAmmountFrom,""]

        WS.append(FileData)
        WB.save(FileName)

        Usuario.objects.filter(id=InfoUser.id).update(available_tickets=F('available_tickets')-1)
        Usuario.objects.filter(id=1).update(fee=F('fee')+FEE)
        
        messages.success(request, 'Solicitud Registrada', extra_tags="title")
        messages.success(request, f'¡EL tiempo de espera aproximado será de {TimeDelta} días Hábiles!', extra_tags="info")
        return redirect(reverse('History'))


def PasswordResetRequestView(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = Usuario.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Solicitud - Restablecer Contraseña"
					email_template_name = "password/password_reset_email.txt"
					c = {
                    'username': user.username,
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
     				'site_name': 'VRT-Fund',
					'protocol': 'https',# http
                    'domain':'vrtfund.com',# 127.0.0.1:8000
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'noreply@vrtfund.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid Header Found')
					return redirect ("/accounts/password_reset/done/")
 
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})



def EmailConfirmView(request, uidb64, token):
   
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            nUser = Usuario.objects.get(pk=uid)

        except Exception as e:
            nUser = None
            with open("/home/savelasquezo/apps/vrt/core/logs/email_err.txt", "a") as f:
                eDate = timezone.now().strftime("%Y-%m-%d %H:%M")
                f.write("EmailConfirm--> {} Error: {}\n".format(eDate, str(e)))

        if nUser and gToken.check_token(nUser, token):
            nUser.is_active = True
            nUser.save()

            return render(request, 'registration/email_confirm.html', {"user": nUser})

        return render(request, 'registration/email_confirm-failed.html', {"user": nUser})
    
    
