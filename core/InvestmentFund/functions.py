from datetime import datetime
from .models import Usuario, FEE, MINAMMOUNT

def GlobalContext(request):
    
    """
    Generates a global context with basic user information for use by all views of the project.
    "InvestmentFund/settings.py"
    TEMPLATES = [{'OPTIONS': {'context_processors': ['InvestmentFund.functions.GlobalContext',],},},]
    """
    
    if request.user.id is not None:
        user = request.user.id
        info_user = Usuario.objects.get(id=user)

        date_now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        date_to_string = info_user.date_expire.strftime('%m/%d/%Y %I:%M %p')
        days_difference = (info_user.date_expire - info_user.date_joined).days
        
        ammount = info_user.ammount
        interest = info_user.interest
        dayli_interest = interest/(100*30)
        
        available = info_user.available

        max_profit = int(ammount*dayli_interest*days_difference)        
        
        ref_available = info_user.ref_available
        
        cash_total = available + ref_available
        total_paid = info_user.paid + info_user.ref_paid
        
        try:
            percent = min(info_user.total_interest/max_profit,1)*100
        except ZeroDivisionError:
            percent = 0
        
        return {
            'username':info_user.username,              #//Nombre de Usuario
            'email':info_user.email,                    #//Correo Electronico
            'full_name':info_user.full_name,            #//Nombre
            'bank':info_user.bank,                      #//Banco
            'bank_account':info_user.bank_account,      #//Cuenta Bancaria
            'fee':FEE,                                  #//Impuesto
            'min_ammount': MINAMMOUNT,                  #//$Min-Retiro
            'ammount':ammount,                          #//Inversion Inicial
            'interest':interest,                        #//Interes Mensual
            'total_paid':total_paid,                    #//Total Abonado
            'available':available,                      #//Disponible Intereses
            'ref_available': ref_available,             #//Disponible Comiciones
            'cash_total':cash_total,                    #//Disponible Total -> Intereses + Comiciones
            'date_expire': date_to_string,              #//Fecha Finalizacion
            'percent': percent,                         #//Porcentaje de Avance ->"Only Intereses"
            'max_profit':max_profit,                    #//Maximo Beneficio Posible
            'date_now_str': date_now_str                #//Hora/Fecha Actual
            }
    return {}   
