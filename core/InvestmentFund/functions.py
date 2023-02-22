from datetime import datetime

from django.utils import timezone
from .models import Usuario, Settings

def GlobalContext(request):
    
    """
    Generates a global context with basic user information for use by all views of the project.
    "InvestmentFund/settings.py"
    TEMPLATES = [{'OPTIONS': {'context_processors': ['InvestmentFund.functions.GlobalContext',],},},]
    """
    
    if request.user.id is not None:
        rUser = request.user

        LocalToday = timezone.now()
        
        InfoUser = Usuario.objects.get(id=rUser.id)
        
        try:
            Setting = Settings.objects.get(Online=True)  
        except:
            Setting = None
            
        Fee = Setting.sFee if Setting else 0
        MinAmmount = Setting.sTicketsAmmount if Setting else 0
        
        TravelExpire = Setting.gTravelDate if Setting else None
        
        try:
            ThisYear = Setting.gTravelDate.replace(month=1, day=1)
        except:
            ThisYear = 0

        GiftDelta = (TravelExpire - LocalToday).days if TravelExpire else None

        TimeDelta = (InfoUser.date_expire - InfoUser.date_joined).days
        TimeExpire = InfoUser.date_expire
            
        Ammount = InfoUser.ammount
        Interet = InfoUser.interest
        
        IntDayli = Interet/(100*30)
        
        InteretTotal = int(Interet*12)
        
        TotalDayli = int(Ammount*IntDayli)
    
        MaxAmmount = int(InfoUser.total_interest + Ammount*IntDayli*(TimeExpire - LocalToday).days)    
        
        TotalCash = int(InfoUser.total_interest + InfoUser.total_ref)
        TotalPaid = int(InfoUser.paid + InfoUser.ref_paid)
        
        TimeKValue = int(((LocalToday - InfoUser.date_joined).days/TimeDelta)*100) if TimeDelta else 0
        
        TimeGValue = int((1 - (GiftDelta/(TravelExpire-ThisYear).days)) * 100) if GiftDelta else 0
        StrTravelExpire = TravelExpire.strftime('%m/%d/%Y %I:%M %p') if TravelExpire else "N/A"
        
        KValue = (InfoUser.total_interest/Ammount)*100 if Ammount else 0
        
        KnobValue = int(min(InfoUser.total_interest/Ammount,1)*100) if Ammount else 0
        KnobText = str(round((KValue / 100)+1, 2)) + "x" if KValue >= 100 else str(round(KValue, 1)) + "%"
        
        TravelState = Setting.IsActive if Setting else False
        WinnerName = Setting.gWinnerName if TravelState else None
   
        return {
            'Setting':Setting,
            'TAX':Fee,                                  
            'MinTicket': MinAmmount,                                  
            'TotalDayli':TotalDayli,      
            'TotalPaid':TotalPaid,                    
            'TotalCash':TotalCash,                                
            'KnobValue':KnobValue,                      
            'KnobText': KnobText,                                      
            'MaxAmmount':MaxAmmount,
            'InteretTotal': InteretTotal,
            'TimeGValue':TimeGValue,
            'TravelState':TravelState,
            'WinnerName':WinnerName,
            'TravelExpire': StrTravelExpire,
            'TimeKValue':TimeKValue, 
            'TimeExpire': TimeExpire.strftime('%m/%d/%Y %I:%M %p')        
            }
    return {}   
