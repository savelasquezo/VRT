
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
    pass
                
if __name__ == '__main__':
    main()