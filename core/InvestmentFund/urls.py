from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

import InvestmentFund.views as views

sitemaps = {
    'News': views.NewsSitemap,
}

urlpatterns = [
    #path("accounts/", include("django.contrib.auth.urls")),

    path('', views.HomeView.as_view(), name='Home'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('accounts/singup/', views.SingupView.as_view(), name='Singup'),
    path('accounts/login/',views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/email/<uidb64>/<token>/', views.EmailConfirmView, name='email_confirm'),
    
    path("accounts/password_reset/", views.PasswordResetRequestView, name="password_reset"),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),    
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      
 
    path('index.php/servicios/basic/', views.BenefitView.as_view(), name='Benefit'),
    path('index.php/servicios/', views.ServicesView.as_view(), name='Services'),
    path('index.php/login/', views.ContentView.as_view(), name='Content'),

    path('investment/premium/', views.InvestPremiumView.as_view(), name='InvEspecial'),
    path('investment/', views.InvestmentView.as_view(), name='Investment'),
    path('terms&conditions/', views.LegalView.as_view(), name='Legal'),    
    path('info/', views.InfoView.as_view(), name='Info'),
    path('info/form/', views.InfoFormView.as_view(), name='InfoForm'),

    path('info/payment/', views.PaymentsView.as_view(), name='Payments'),
    path('info/payment/banktransfer/', views.PaymentsBanks.as_view(), name='PaymentsBanks'),

    path('@', views.ComingSoonView, name='ComingSoon'),

    path('accounts/admin/', views.InterfaceView.as_view(), name='Interface'),
    path('accounts/admin/ticket/', views.TicketFormView.as_view(), name='Tickets'),
    path('accounts/admin/history/', views.HistoryListView.as_view(), name='History'),

    path('accounts/admin/gift/', views.GiftView.as_view(), name='Gift'),
    path('accounts/admin/gift/ticket/', views.GiftTicketView.as_view(), name='GiftTicket'),

    path('services/admin/', views.AdminServicesHistory.as_view(), name='svAdmin'), #AdminServices
    path('services/admin/add', views.AdminServicesAdd.as_view(), name='svAdminAdd'),
    path('services/admin/user', views.AdminServicesUser.as_view(), name='svAdminUser'),
    path('services/admin/history', views.AdminServicesHistory.as_view(), name='svAdminHistory'), ##

    path('test/', views.TestView.as_view(), name='test'),


]


