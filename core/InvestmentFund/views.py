import os
from openpyxl import Workbook
from openpyxl import load_workbook

from datetime import datetime, timedelta

from django.utils import timezone
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError

from .models import Usuario, Tickets, FEE

class HomeView(TemplateView):
    template_name='home/home.html'

    def post(self, request, *args, **kwargs):
        iUsername = request.POST['username']
        iPass = request.POST['password']
        iFullName = request.POST['name']
        iEmail = request.POST['email']

        LastID = Usuario.objects.latest('id').id + 1
        
        try:
            nUser = Usuario.objects.create(
                username = iUsername,
                full_name = iFullName,
                email = iEmail,
                codigo = LastID
            )
            
            nUser.set_password(iPass)
            nUser.save()
            
            #login(request, nUser) ---> Usuario Inactivo Default

            messages.success(request, '¡Registro Exitoso!', extra_tags="title")
            messages.success(request, f'Comuniquese con un Administrador para activar su Cuenta', extra_tags="info")
            
        except IntegrityError:
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, f'El Usuario ingresado actualmente esta registrado', extra_tags="info")         
        
        return redirect(reverse('Home'))


class SingupView(TemplateView):
    template_name='registration/singup.html'
    
class InvestmentView(LoginRequiredMixin, TemplateView):
    template_name='home/investment.html'
    
class ContentView(LoginRequiredMixin, TemplateView):
    template_name='home/content.html'

class BenefitView(LoginRequiredMixin, TemplateView):
    template_name='home/benefit.html'

class InterfaceView(LoginRequiredMixin, TemplateView):
    template_name='interface/interface.html'

class LegalView(LoginRequiredMixin, TemplateView):
    template_name='home/legal.html'

class InfoView(LoginRequiredMixin, TemplateView):
    template_name='home/info.html'

class TicketFormView(LoginRequiredMixin, TemplateView):
    template_name='interface/tickets.html'

class HistoryListView(LoginRequiredMixin, TemplateView):
      
    template_name='interface/history.html'

    def days_until_next_month(self):
        Today = datetime.now()
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
            messages.error(request, '¡Ha exedigo el numero de retiros mensuales!', extra_tags="info")
            return redirect(reverse('History'))

        if rAmmountFrom == "f1":
            rAmmountFrom = "Intereses"
            
            if rAmmount > InfoUser.available:
                messages.error(request, 'ERROR', extra_tags="title")
                messages.error(request, 'La solicitud no se ha podiso procesar', extra_tags="info")
                return redirect(reverse('History'))
            
            Usuario.objects.filter(id=InfoUser.id).update(
                available=F('available')-rAmmount,
                paid=F('paid')+rAmmount
                )

        if rAmmountFrom == "f2":
            rAmmountFrom = "Comisiones"
            
            if rAmmount > InfoUser.ref_available:
                messages.error(request, 'ERROR', extra_tags="title")
                messages.error(request, 'La solicitud no se ha podiso procesar', extra_tags="info")
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
                messages.error(request, 'La solicitud no se ha podiso procesar', extra_tags="info")
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
        TimeDelta = self.days_until_next_month()
        
        messages.success(request, 'Solicitud Registrada', extra_tags="title")
        messages.success(request, f'EL tiempo de espera aproximado sera de {TimeDelta} dias habiles', extra_tags="info")
        return redirect(reverse('History'))

