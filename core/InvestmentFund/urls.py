from django.urls import path, include
from .views import HomeView, InterfaceView, TicketFormView, HistoryListView, InvestmentView, ContentView, BenefitView, SingupView, LegalView

urlpatterns = [

    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/singup/', SingupView.as_view(), name='Singup'),

    path('', HomeView.as_view(), name='Home'),

    path('index.php/servicios/', BenefitView.as_view(), name='Benefit'),
    path('index.php/contenido/', ContentView.as_view(), name='Content'),
    path('investment/', InvestmentView.as_view(), name='Investment'),
    path('terms&conditions/', LegalView.as_view(), name='Legal'),

    path('accounts/profile/', InterfaceView.as_view(), name='Interface'),
    path('accounts/profile/ticket/', TicketFormView.as_view(), name='Tickets'),
    path('accounts/profile/history/', HistoryListView.as_view(), name='History'),
]


