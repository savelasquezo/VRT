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
        ordering = {"Usuarios": 1, "Tickets": 2, "Solicitudes": 3, "Asociaciones": 4, "Mensajes": 5, "Noticias": 6, "Configuraciones": 7,"Grupos": 0}
        app_dict = self._build_app_dict(request, app_label)

        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list

admin_site = MyAdminSite()
admin.site = admin_site
admin_site.site_header = "VRTFUND"


class FilesInline(admin.StackedInline):
    
    model = model.Files
    extra = 0
    fieldsets = ((" ", {"fields": (("file",),)}),)


class UserBaseAdmin(UserAdmin):

    list_display = (
        "username",
        "full_name",
        "codigo",
        "ammount",
        "interest",
        "available",
        "date_joined",
        "is_operating",
        )

    fAutenticationSuperUser = {"fields": (
        ("codigo","available_tickets","is_staff","is_operating","is_dirver"),
        ("password")
        )}

    fAutenticationUser = {"fields": (
        ("codigo","available_tickets","is_operating"),
        ("password")
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
        ("date_joined")
        )}

    fInterest = {"fields": (
        ("available","paid"),
        "total_interest"
        )}

    fReferees = {"fields": (
        ("ref_available","ref_paid"),
        "total_ref"
        )}


    fRefInformation = {"fields": (
            ("ref_id","ref_name"),
            ("ref_total","ref_interest")
        )}

    fGroups = {"fields": (
            "groups",
        )}
    
    fieldsets = (
        ("Autenticacion", fAutenticationSuperUser),
        ("Informacion", fInformation),
        ("Inversion", fInvestment),
        ("Intereses", fInterest),
        ("Comiciones", fReferees),
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

    list_filter = ["date_joined","is_operating"]
    search_fields = ['codigo','username','full_name']

    
    es_formats.DATETIME_FORMAT = "d M Y"

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return (
                ("Autenticacion", self.fAutenticationUser),
                ("Informacion", self.fInformation),
                ("Inversion", self.fInvestment),
                ("Intereses", self.fInterest),
                ("Comiciones", self.fReferees),
                ("Informacion del Asociado", self.fRefInformation)
            )
        return super().get_fieldsets(request, obj)





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

    readonly_fields=["username","tAmmount","tBank","tBankAccount","tAmmountFrom","date","CommentText",]


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
        ("date_joined"),
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

    readonly_fields=["username","invoice","full_name","country","ammount","email","phone","bank","bank_account","CommentText","staff","staff_cod"]


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

    readonly_fields=["full_name","email","date","messages"]



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
        "IsActive"
        )

    fConfig = {"fields": (
        ("pName","pTitle"),
        ("pURL","IsActive"),
        ("pDiscount"),
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



class SettingsAdmin(admin.ModelAdmin):

    inlines = [FilesInline]

    list_display = (
        "id",
        "exchange",
        "sName",
        "sFee",
        "sTickets",
        "sTicketsAmmount",
        "Online"
        )

    fConfig = {"fields": (
        ("sName","Online","exchange"),
        ("sFee","sFeeAmmount"),
        ("sTickets","sTicketsAmmount"),
        )}

    fTravel = {"fields": (
        ("gWinnerName","gTravelName"),
        ("gTravelDate","IsActive"),
        "gTravelBanner",
        )}

    list_filter = ["Online"]
    search_fields = ['sName']


    fieldsets = (
        ("Configuracion", fConfig),
        ("VRT-Travel", fTravel)
        )

    def has_add_permission(self, request):
         return False if model.Settings.objects.exists() else True



admin.site.register(Group)

admin.site.register(model.Usuario, UserBaseAdmin)

admin.site.register(model.Tickets, TicketsAdmin)

admin.site.register(model.InvestRequests, InvestRequestsAdmin)
admin.site.register(model.Associate, AssociateAdmin)
admin.site.register(model.Messages, MessagesAdmin)
admin.site.register(model.News, NewsAdmin)
admin.site.register(model.Settings, SettingsAdmin)

