from datetime import datetime
from django.utils import timezone
from .models import Usuario, FEE, MINAMMOUNT

def GlobalContext(request):
    
    """
    Generates a global context with basic user information for use by all views of the project.
    "InvestmentFund/settings.py"
    TEMPLATES = [{'OPTIONS': {'context_processors': ['InvestmentFund.functions.GlobalContext',],},},]
    """
    
    if request.user.id is not None:
        rUser = request.user
        InfoUser = Usuario.objects.get(id=rUser.id)

        date_now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        date_to_string = InfoUser.date_expire.strftime('%m/%d/%Y %I:%M %p')
        days_difference = (InfoUser.date_expire - InfoUser.date_joined).days
        
        now = timezone.now()
            
        ammount = InfoUser.ammount
        interest = InfoUser.interest
        dayli_interest = interest/(100*30)
        total_dayli_interest = int(ammount*dayli_interest)
        
        available = InfoUser.available

        max_profit = int(ammount*dayli_interest*days_difference)        
        
        ref_available = InfoUser.ref_available
        
        cash_total = InfoUser.total_interest + InfoUser.total_ref
        total_paid = InfoUser.paid + InfoUser.ref_paid
        
        try:
            time_percent = int(((now - InfoUser.date_joined).days/days_difference)*100)
            knobvalue = int(min(InfoUser.total_interest/ammount,1)*100)
            percent = (InfoUser.total_interest/ammount)*100
            
            if percent >= 100:
                knobtext = str(round((percent/100),2))+"x"
                
            if percent < 100:
                knobtext = str(round(percent,2))+"%"
            
            
        except ZeroDivisionError:
            time_percent = 0
            knobvalue = 0
            knobtext = 0
            percent = 0
        
        return {
            'username':InfoUser.username,               #//Nombre de Usuario
            'email':InfoUser.email,                     #//Correo Electronico
            'full_name':InfoUser.full_name,             #//Nombre
            'bank':InfoUser.bank,                       #//Banco
            'bank_account':InfoUser.bank_account,       #//Cuenta Bancaria
            'fee':FEE,                                  #//Impuesto
            'min_ammount': MINAMMOUNT,                  #//$Min-Retiro
            'ammount':ammount,                          #//Inversion Inicial
            'interest':interest,                        #//Interes Mensual
            'dayli_interest':total_dayli_interest,      #//Interes Diario
            'total_paid':total_paid,                    #//Total Abonado
            'available':available,                      #//Disponible Intereses
            'ref_available': ref_available,             #//Disponible Comiciones
            'cash_total':cash_total,                    #//Total -> Intereses + Comiciones
            'date_expire': date_to_string,              #//Fecha Finalizacion
            'knobvalue':knobvalue,                      #//Valor WidgetBar
            'knobtext': knobtext,                       #//Porcentaje de Avance ->"Only Intereses"
            'time_percent':time_percent,                #//Porcentaje de Avance Tiempo
            'max_profit':max_profit,                    #//Maximo Beneficio Posible
            'date_now_str': date_now_str                #//Hora/Fecha Actual
            }
    return {}   
