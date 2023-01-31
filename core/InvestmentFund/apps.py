from django.apps import AppConfig


class InvestmentfundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InvestmentFund'
    verbose_name = "Fondo de Inversion"

    def ready(self):
        from InvestmentFund.signals import investment_add_record
        from InvestmentFund.signals import tickets_add_record