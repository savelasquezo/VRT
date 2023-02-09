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

        NowToday = timezone.now()
        InfoUser = Usuario.objects.get(id=rUser.id)

        TimeDelta = (InfoUser.date_expire - InfoUser.date_joined).days
        TimeExpire = InfoUser.date_expire
            
        Ammount = InfoUser.ammount
        Interet = InfoUser.interest
        
        IntDayli = Interet/(100*30)
        
        EA = int(Interet*12)
        
        TotalDayli = int(Ammount*IntDayli)
    
        MaxAmmount = int(InfoUser.total_interest + Ammount*IntDayli*(TimeExpire - NowToday).days)    
        
        TotalCash = int(InfoUser.total_interest + InfoUser.total_ref)
        TotalPaid = int(InfoUser.paid + InfoUser.ref_paid)
        
        TimeKValue = int(((NowToday - InfoUser.date_joined).days/TimeDelta)*100) if TimeDelta else 0
        KValue = (InfoUser.total_interest/Ammount)*100 if Ammount else 0
        
        KnobValue = int(min(InfoUser.total_interest/Ammount,1)*100) if Ammount else 0
        KnobText = str(round((KValue / 100)+1, 2)) + "x" if KValue >= 100 else str(round(KValue, 1)) + "%"
   
        return {
            'TAX':FEE,                                  
            'MinTicket': MINAMMOUNT,                                  
            'TotalDayli':TotalDayli,      
            'TotalPaid':TotalPaid,                    
            'TotalCash':TotalCash,                                
            'KnobValue':KnobValue,                      
            'KnobText': KnobText,                       
            'TimeKValue':TimeKValue,                
            'MaxAmmount':MaxAmmount,
            'EA': EA,
            'TimeExpire': TimeExpire.strftime('%m/%d/%Y %I:%M %p')        
            }
    return {}   
