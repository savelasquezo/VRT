from django.urls import path, include
import InvestmentFund.views as views

from django.contrib.auth import views as auth_views

urlpatterns = [

    #path("accounts/", include("django.contrib.auth.urls")),
    path('', views.HomeView.as_view(), name='Home'),
    
    path('accounts/singup/', views.SingupView.as_view(), name='Singup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      
    path("accounts/password_reset/", views.PasswordResetRequestView, name="password_reset"),

    path('index.php/servicios/', views.BenefitView.as_view(), name='Benefit'),
    path('index.php/login/', views.ContentView.as_view(), name='Content'),

    path('investment/', views.InvestmentView.as_view(), name='Investment'),
    path('terms&conditions/', views.LegalView.as_view(), name='Legal'),    
    path('info/', views.InfoView.as_view(), name='Info'),
    path('info/form', views.InfoFormView.as_view(), name='InfoForm'),


    path('accounts/admin/', views.InterfaceView.as_view(), name='Interface'),
    path('accounts/admin/ticket/', views.TicketFormView.as_view(), name='Tickets'),
    path('accounts/admin/history/', views.HistoryListView.as_view(), name='History'),
]


