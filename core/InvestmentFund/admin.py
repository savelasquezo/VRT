from ckeditor.widgets import CKEditorWidget

from django.db import models
from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

import InvestmentFund.models as model

class MyAdminSite(admin.AdminSite):
    index_title = 'Panel Administrativo'
    verbose_name = "VRTFUND"


    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site. NewMetod for ordering Models
        """
        ordering = {"Usuarios": 1, "Tickets": 2, "Solicitudes": 3, "Asociaciones": 4, "Mensajes": 5, "Noticias": 6, "Configuraciones": 7,"Groups": 0}
        app_dict = self._build_app_dict(request, app_label)

        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list




admin_site = MyAdminSite()
admin.site = admin_site

admin_site.site_header = "VRTFUND"

class ScheduleInline(admin.StackedInline):

    model = model.Schedule
    extra = 0

    fInfo = {"fields": (
            ("driver","date"),
            ("addres_from","addres_to"),
            ("status","paid")
        )}

    fieldsets = (
        (" ", fInfo),
        )
    
    search_fields = ['username']
    
    list_filter = []
    filter_horizontal = []
    es_formats.DATETIME_FORMAT = "d M Y H:i"


class UserBaseAdmin(UserAdmin):

    inlines = [ScheduleInline]

    list_display = (
        "username",
        "full_name",
        "codigo",
        "ammount",
        "interest",
        "available",
        "date_joined",
        "date_expire",
        "is_operating",
        )

    fAutenticationSuperUser = {"fields": (
        ("codigo","available_tickets","is_staff","is_dirver","is_driving"),
        ("is_active","is_operating"),
        ("password")
        )}

    fAutenticationUser = {"fields": (
        ("codigo","is_active","available_tickets","is_driving"),
        "password",
        ("is_operating","is_dirver")
        )}

    fInformation = {"fields": (
        ("full_name","country"),
        ("email","phone"),
        "avatar"
        )}
    
    fInvestment = {"fields": (
        ("ammount","interest"),
        ("bank",
        "bank_account"),
        ("date_joined","date_expire")
        )}

    fInterest = {"fields": (
        ("available","paid"),
        "total_interest"
        )}

    fReferees = {"fields": (
        ("ref_available","ref_paid"),
        "total_ref"
        )}

    frank = {"fields": (
        "user_rank",
        ("rank_points","rank_used"),
        "rank_total"
        )}

    fRefInformation = {"fields": (
            ("ref_id","ref_name"),
            ("ref_total","ref_interest")
        )}

    fGroups = {"fields": (
            "groups",
        )}
    
    fieldsets = (
        ("Autenticacion", fAutenticationUser),
        ("Informacion", fInformation),
        ("Inversion", fInvestment),
        ("Intereses", fInterest),
        ("Comiciones", fReferees),
        ("VRT-Beneficios", frank),
        ("Informacion del Asociado", fRefInformation),
        ("Autorizaciones", fGroups)
        )

    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": (("username","codigo"), "password1", "password2"),
            },
        ),
    )

    list_filter = ["date_joined","date_expire","is_operating"]
    search_fields = ['rName']

    radio_fields = {'user_rank': admin.HORIZONTAL}
    
    es_formats.DATETIME_FORMAT = "d M Y"


    def get_fieldsets(self, request, obj=None):
        if obj and obj.is_superuser:
            return (
                ("Autenticacion", self.fAutenticationSuperUser),
                ("Informacion", self.fInformation),
                ("Inversion", self.fInvestment),
                ("Intereses", self.fInterest),
                ("Comiciones", self.fReferees),
                ("VRT-Beneficios", self.frank),
                ("Informacion del Asociado", self.fRefInformation)
            )
        return super().get_fieldsets(request, obj)

    
class UserRankAdmin(admin.ModelAdmin):

    list_display = (
        "rName",
        "rTravelGift",
        "rVacations",
        "rGiftCard",
        "rSimCard",
        "rAdvisory"
        )

    list_filter = ["rTravelGift","rVacations","rGiftCard","rSimCard","rAdvisory"]
    search_fields = ['rName']
  
    fCategory = {"fields": (
        "rName",
        ("rTravelGift","rVacations","rGiftCard","rSimCard","rAdvisory"),
        )}

    fInformation = {"fields": (
        
        )}
    
    fieldsets = (
        ("Caracteristicas", fCategory),
        )
    
    radio_fields = {'rName': admin.HORIZONTAL}

class MessagesAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "email",
        "date",
        "is_view",
        )

    list_filter = ["date","is_view"]
    search_fields = ['full_name']
  
    fInfo = {"fields": (
        ("full_name","is_view"),
        ("email","date"),
        "messages",
        )}
    
    fieldsets = (
        ("Informacion", fInfo),
        )

    def has_add_permission(self, request, obj=None):
            return False

class TicketsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "tAmmount",
        "tBank",
        "tBankAccount",
        "tBankTicket",
        "rState"
        )


    fTickets = {"fields": (
        ("username","rState"),
        ("tAmmount","tAmmountFrom"),
        ("tBank","tBankAccount"),
        ("date","tBankTicket"),
        "CommentText"
        )}

    list_filter = ["date","rState","tBank"]
    search_fields = ['username']

    radio_fields = {'rState': admin.HORIZONTAL}

    fieldsets = (
        ("Caracteristicas", fTickets),
        )

    def has_add_permission(self, request, obj=None):
            return False


class InvestRequestsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "invoice",
        "full_name",
        "ammount",
        "interest",
        "staff",
        "date_joined",
        "rState"
        )


    fInvestRequestsStaff = {"fields": (
        ("username"),
        ("invoice","codigo"),
        ("full_name","country"),
        ("ammount","interest"),
        ("email","phone"),
        ("bank","bank_account"),
        ("date_joined","date_expire"),
        "CommentText"
        )}

    fInvestRequestsSuperUser = {"fields": (
        ("staff","staff_cod"),
        "rState",
        )}
    

    list_filter = ["date_joined","rState"]
    superlist_filter = ["staff","rState","date_joined"]
    
    search_fields = ['username']

    radio_fields = {'rState': admin.HORIZONTAL}
    es_formats.DATETIME_FORMAT = "d M Y"
    
    fieldsets = (
        ("Informacion", fInvestRequestsStaff),
        ("Autorizacion",fInvestRequestsSuperUser),
        )

    """def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                ("Informacion", self.fInvestRequestsStaff),
                ("Autorizacion", self.fInvestRequestsSuperUser),
            )
        return super().get_fieldsets(request, obj)"""

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.staff = request.user.username
            obj.staff_cod = request.user.codigo
            super().save_model(request, obj, form, change)
            return
        
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
            
        if not request.user.is_superuser:
            return model.InvestRequests.objects.filter(staff_cod = request.user.codigo)

        qs = self.model._default_manager.get_queryset()

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
                
        return qs

    """def get_list_filter(self, request):

        if not request.user.is_superuser:
            return self.list_filter
        
        return self.superlist_filter"""


class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "sType",
        "sPts",
        "date_join",
        "date_approved",
        "sState"
        )

    fServices = {"fields": (
        ("username","sState"),
        ("sType","sPts"),
        ("date_join","date_approved"),
        ("sCode"),
        "CommentText"
        )}

    list_filter = ["date_join","date_approved","sType"]
    search_fields = ['username']

    radio_fields = {'sState': admin.HORIZONTAL}

    fieldsets = (
        ("Caracteristicas", fServices),
        )

    def has_add_permission(self, request, obj=None):
            return False


class SettingsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usdConvert",
        "sName",
        "sFee",
        "sTickets",
        "sTicketsAmmount",
        "sState",
        "Online"
        )

    fConfig = {"fields": (
        ("sName","Online","sState"),
        ("sFee","sFeeAmmount"),
        ("sTickets","sTicketsAmmount"),
        "sDriverPoints",
        "usd_convert",
        )}

    fTravel = {"fields": (
        ("gWinnerName"),
        ("gTravelName","IsActive"),
        "gTravelBanner",
        "gTravelDate"
        )}

    list_filter = ["Online"]
    search_fields = ['sName']


    fieldsets = (
        ("Configuracion", fConfig),
        ("VRT-Travel", fTravel)
        )


class NewsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "description",
        "date",
        )

    fNews = {"fields": (
        ("name","date"),
        "image",
        "description",
        )}

    list_filter = ["date"]
    search_fields = ['name']


    fieldsets = (
        ("Informacion", fNews),
        )
    


class AssociateAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "pName",
        "pTitle",
        "pDiscount",
        "pPtsMin",
        "IsActive"
        )

    fConfig = {"fields": (
        ("pName","pTitle"),
        ("pPtsMin","IsActive"),
        ("pURL","pDiscount"),
        ("pInfo","pInfoAdd")
        )}

    fTravel = {"fields": (
        "pCard",
        "pBanner"
        )}

    list_filter = ["IsActive"]
    search_fields = ['pName']


    fieldsets = (
        ("Informacion", fConfig),
        ("Multimedia", fTravel)
        )


admin.site.register(Group)

admin.site.register(model.Usuario, UserBaseAdmin)
#admin.site.register(UserRank, UserRankAdmin)
admin.site.register(model.Tickets, TicketsAdmin)
#admin.site.register(Services, ServicesAdmin)
admin.site.register(model.InvestRequests, InvestRequestsAdmin)
admin.site.register(model.Associate, AssociateAdmin)
admin.site.register(model.Messages, MessagesAdmin)
admin.site.register(model.News, NewsAdmin)
admin.site.register(model.Settings, SettingsAdmin)

