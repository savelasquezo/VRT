
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from datetime import date


from django.utils import timezone
from django.db.models import F
from django.utils import timezone

from openpyxl import Workbook
from openpyxl import load_workbook

from InvestmentFund.models import Usuario

def main():
    
        InfoUser = Usuario.objects.all()
        Usuario.objects.filter(date_expire__lte=timezone.now()).update(is_operating=False)

        for nUser in InfoUser:

            if nUser.is_operating:

                CUser = Usuario.objects.filter(id=nUser.id)
                    
                if date.today().day == 1:
                    CUser.update(available_tickets=3)

                cAmmount = int(nUser.ammount)
                cTotalInterest = int(nUser.total_interest)
                cPaid = int(nUser.paid)
                cPaidRef = int(nUser.ref_paid)

                cInterest = float((nUser.interest)/(100*30))
                cInterestRef = float((nUser.ref_interest)/(100*30))

                cValue = int(cAmmount*(cInterest))
                cValueRef = int(cAmmount*(cInterestRef))
                
                cAvailable = int(cTotalInterest-cPaid + cValue)

                CUser.update(
                    available=cAvailable,
                    total_interest=F('total_interest') + cValue,
                    ref_total=F('ref_total') + cValueRef
                    )

                UserRef = Usuario.objects.filter(ref_id= nUser.codigo)
                mAviableUserRef = 0
                
                for mUser in UserRef:
                    mAviableUserRef += int(mUser.ref_total)

                mAviableUserTotal = mAviableUserRef - cPaidRef
                
                CUser.update(
                    ref_available=mAviableUserTotal,
                    total_ref=mAviableUserRef
                    )

                CUser.update(total=F('total_ref') + F('total_interest'))

                FileName = 'InvestmentFund/users/'+ nUser.username + '.xlsx'


                if not os.path.exists(FileName):
                    WB = Workbook()
                    WS = WB.active
                    WS.append(["Tipo","Fecha", "Interes", "Referido", "Ticket", "Actual"])
                else:
                    WB = load_workbook(FileName)
                    WS = WB.active

                NowToday = timezone.now().strftime("%Y-%m-%d %H:%M")

                FileData = [1, NowToday, cValue, cValueRef, 0, cAvailable]

                WS.append(FileData)
                WB.save(FileName)
                
if __name__ == '__main__':
    main()