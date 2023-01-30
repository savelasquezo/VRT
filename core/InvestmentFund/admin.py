from django.contrib import admin

from django.conf.locale.es import formats as es_formats
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Usuario, UserRank, Tickets, InvestRequests


class MyAdminSite(admin.AdminSite):
    index_title = 'Panel Administrativo'
    verbose_name = "VRTFUND"


    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site. NewMetod for ordering Models
        """
        ordering = {"Usuarios": 1, "Tickets": 2, "Solicitudes": 3, "Status": 4,"Grupos": 5}
        app_dict = self._build_app_dict(request, app_label)

        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list




admin_site = MyAdminSite()
admin.site = admin_site

admin_site.site_header = "VRTFUND"



class UserBaseAdmin(UserAdmin):

    list_display = (
        "username",
        "full_name",
        "codigo",
        "ammount",
        "interest",
        "date_joined",
        "date_expire",
        "ref_id",
        "is_operating",
        )

    fAutenticationSuperUser = {"fields": (
        ("codigo", "fee", "available_tickets"),
        "password"
        )}

    fAutenticationUser = {"fields": (
        ("codigo","is_active","available_tickets"),
        "password",
        ("is_operating","is_staff")
        )}
    
    fInformation = {"fields": (
        ("full_name",
        "country"),
        ("email",
        "phone")
        )}
    
    fInvestment = {"fields": (
        ("user_rank","interest"),
        ("ammount"),
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
        ("Informacion del Referido", fRefInformation),
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
                ("Informacion del Referido", self.fRefInformation)
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
        "full_name",
        "ammount",
        "interest",
        "staff",
        "date_joined",
        "rState"
        )


    fInvestRequestsStaff = {"fields": (
        "username",
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
        )

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                ("Informacion", self.fInvestRequestsStaff),
                ("Autorizacion", self.fInvestRequestsSuperUser),
            )
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.staff = request.user.username
            obj.staff_cod = request.user.codigo
            super().save_model(request, obj, form, change)
            return
        
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
            
        if not request.user.is_superuser:
            return InvestRequests.objects.filter(staff_cod = request.user.codigo)

        qs = self.model._default_manager.get_queryset()

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
                
        return qs

    def get_list_filter(self, request):

        if not request.user.is_superuser:
            return self.list_filter
        
        return self.superlist_filter


admin.site.register(Group)

admin.site.register(Usuario, UserBaseAdmin)
admin.site.register(UserRank, UserRankAdmin)
admin.site.register(Tickets, TicketsAdmin)
admin.site.register(InvestRequests, InvestRequestsAdmin)



