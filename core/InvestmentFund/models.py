from datetime import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

lst_ranks = (('Silver','Silver'),('Gold','Gold'),('Platinum','Platinum'))
lst_sts = (('Pendiente','Pendiente'),('Aprobado','Aprobado'),('Denegado','Denegado'),('Error','Error'))

list_status = (('Completado','Completado'),('Pendiente','Pendiente'),('Cancelado','Cancelado'))

def CustomUpload(instance, filename):
    return f"media/news/{filename}"

class Usuario(AbstractUser):
    """
    Custom user model inherited from abstractly user.
    "InvestmentFund/settings.py"
    AUTH_USER_MODEL = 'InvestmentFund.Usuario'
    USERNAME_FIELD = 'username'
    """

    username_validator = UnicodeUsernameValidator()
    
    id = models.AutoField(primary_key=True, verbose_name="id")

    codigo = models.CharField(_("Codigo"),max_length=64 ,unique=True,
                help_text=_("Codigo Impreso en las Credenciales"))
    
    username = models.CharField(_("Usuario"),max_length=64,unique=True, validators=[username_validator],
                help_text=_("Caracters Max-64, Únicamente letras, dígitos y @/./+/-/_"),
                error_messages={"unique": _("¡Usuario Actualmente en Uso!"),},)

    avatar = models.ImageField(_("Avatar/Foto"), upload_to="InvestmentFund/uploads/avatars/", height_field=None, width_field=None, max_length=128, blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name="")
    is_staff = models.BooleanField(_("¿Staff?"),default=False)

    is_dirver = models.BooleanField(_("¿Conductor?"),default=False)
    is_driving = models.BooleanField(_("¿Ocupado?"),default=False)

    is_operating = models.BooleanField(_("¿Activo?"),default=False,)

    available_tickets = models.IntegerField(_("Tickets"),blank=True,default=3,
                help_text=_("Tickets Disponibles"),)

    full_name = models.CharField(_("Nombre/Apellido"), max_length=64, blank=True)
    email = models.EmailField(_("E-mail"), blank=True)
    phone = models.CharField(_("Telefono"), max_length=64, blank=True)
    
    country = models.CharField(_("Ubicacíon"),max_length=64,blank=True)
    
    ammount = models.PositiveBigIntegerField(_("Inversion"),blank=True,default=0,
                help_text=_("Volumen de Capital Invertido ($COP)"),)
    
    bank = models.CharField(_("Banco"), max_length=32,blank=True,null=True,
                help_text=_("Banco/Fundacion o Metodo al cual se realizaran los pagos."),)
    
    bank_account = models.CharField(_("Wallet/Cuenta"), max_length=32,blank=True,)


    interest = models.DecimalField(_("Interes"), max_digits=5, decimal_places=2, blank=True,default=0,
                help_text=_("Volumen de Retorno Mensual (%)"),)

    date_joined = models.DateTimeField(_("Ingreso"), default=timezone.now)
    date_expire = models.DateTimeField(_("Finaliza"), default=timezone.now)
    
    available = models.PositiveBigIntegerField(_("Acumulado"),blank=True,default=0,
                help_text=_("$Disponible Generado en Intereses"),)
    
    paid = models.PositiveBigIntegerField(_("Abonado"),blank=True,default=0,
                help_text=_("$Abonado al Cliente"),)

    total_interest = models.PositiveBigIntegerField(_("Total"),blank=True,default=0,
                help_text=_("$Total Generado en Intereses"),)

    ref_available = models.PositiveBigIntegerField(_("Acumulado Ref"),blank=True,default=0,
                help_text=_("$Disponible Generado de Comiciones"),)

    ref_paid = models.PositiveBigIntegerField(_("Abonado Ref"),blank=True,default=0,
                help_text=_("$Abonado de Comiciones"),)

    total_ref = models.PositiveBigIntegerField(_("Total Ref"),blank=True,default=0,
                help_text=_("$Total Generado de Comiciones"),)

    total = models.PositiveBigIntegerField(_("Total"),blank=True,default=0,
                help_text=_("$Total Generado ($COP)"),)

    ref_id = models.CharField(_("Codigo"), max_length=32, blank=True)
    ref_name = models.CharField(_("Nombre"), max_length=64, blank=True)
    ref_interest = models.DecimalField(_("Interes"), max_digits=5, decimal_places=2, blank=True,default=0,
        help_text=_("Comisiones Mensuales x Asociado (%)"),)

    ref_total = models.PositiveBigIntegerField(_("Total"),blank=True,default=0,
                help_text=_("Capital Generado al Asociado ($COP)"),)

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")


class Tickets(models.Model):
        
    id = models.AutoField(primary_key=True, verbose_name="Ticket")
    username = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name="Usuario")
    tAmmount = models.PositiveBigIntegerField(_("Volumen"),blank=False,null=False,default=0,
        help_text=_("Volumen de Capital Solicitado ($COP)"),)

    tAmmountFrom = models.CharField(_("Origen"), max_length=32,blank=False,null=False,
        help_text=_("Origen del Volumen"),)
    
    tBank = models.CharField(_("Banco"), max_length=32,blank=False,null=False,
        help_text=_("Banco/Fundacion o Metodo al cual se realizaran los pagos."))
    
    tBankAccount = models.CharField(_("#Cuenta"), max_length=32,blank=False,null=False)
    
    date = models.DateTimeField(_("Fecha"), default=timezone.now)
    
    tBankTicket = models.CharField(_("Voucher"), max_length=32,blank=True,
        help_text=_("Referencia/Voucher Transaccion"))

    CommentText = models.TextField(_("Comentarios"),max_length=256,blank=True,null=True)

    rState = models.CharField(_("Estado"), choices=lst_sts, default="Pendiente", max_length=16)
    
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return "Ticket: %s" % (self.pk)
    
    
class InvestRequests(models.Model):

    username = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'is_operating': False})

    codigo = models.CharField(_("Codigo"),max_length=64 ,unique=True,
            help_text=_("Codigo Impreso en las Credenciales"))

    invoice = models.CharField(_("Factura"),max_length=64 ,unique=False, default="N/A", blank=False, null=False,
            help_text=_("Facturacion Electronica"))

    full_name = models.CharField(_("Nombre/Apellido"), max_length=64, blank=True)
    email = models.EmailField(_("E-mail"), blank=True)
    country = models.CharField(_("Ubicacíon"),max_length=64,blank=True)
    phone = models.CharField(_("Telefono"), max_length=64, blank=True)  

    ammount = models.PositiveBigIntegerField(_("Inversion"),blank=True,default=0,
                help_text=_("Volumen de Capital a Invertir ($COP)"),)
    
    interest = models.DecimalField(_("Interes"), max_digits=5, decimal_places=2, blank=True,default=0,
                help_text=_("Volumen de Retorno Mensual (%)"),)
    
    bank = models.CharField(_("Banco"), max_length=32, blank=True, null=True,
                help_text=_("Banco/Fundacion o Metodo al cual se realizaran los pagos."),)
    
    bank_account = models.CharField(_("Wallet/Cuenta"), max_length=32,blank=True,)

    CommentText = models.TextField(_("Comentarios"),max_length=256,blank=True,null=True)

    staff = models.CharField(_("Staff"), max_length=64, blank=True)
    staff_cod = models.CharField(_("Codigo Staff"),max_length=64,
                help_text=_("Codigo del Usuario Staff Afiliador"))

    date_joined = models.DateTimeField(_("Ingreso"), default=timezone.now)
    date_expire = models.DateTimeField(_("Finaliza"), default=timezone.now)

    rState = models.CharField(_("Estado"), choices=lst_sts, default="Pendiente", max_length=16)

    class Meta:
        verbose_name = _("Solicitud")
        verbose_name_plural = _("Solicitudes")

    def __str__(self):
        return "Solicitud: %s" % (self.pk)   
    
    
    
class Services(models.Model):
        
    id = models.AutoField(primary_key=True, verbose_name="ID")
    username = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name="Usuario")
    sPts = models.PositiveBigIntegerField(_("PTS"),blank=False,null=False,default=0,
        help_text=_("Cantidad de VRTs Usados"),)

    sType = models.CharField(_("Origen"), max_length=32,blank=False,null=False,
        help_text=_("Servicio Solicitado"),)
    
    sCode = models.CharField(_("Codigo"), max_length=32,blank=True,
        help_text=_("Referencia/Codigo Promocional"))

    date_join = models.DateTimeField(_("Solicitado"), default=timezone.now)
    date_approved = models.DateTimeField(_("Modificado"), default=timezone.now)

    CommentText = models.TextField(_("Comentarios"),max_length=256,blank=True,null=True)

    sState = models.CharField(_("Estado"), choices=lst_sts, default="Pendiente", max_length=16)
    
    class Meta:
        verbose_name = _("Servicio")
        verbose_name_plural = _("Servicios")

    def __str__(self):
        return "Servicio: %s" % (self.pk)


class Settings(models.Model):
        
    id = models.AutoField(primary_key=True, verbose_name="ID")
    Online = models.BooleanField(_("Status"),default=True,unique=True)

    exchange = models.PositiveIntegerField(_("USD"),default=5000,
                help_text=_("Tasa de Cambio ($COP)"),)

    sState = models.BooleanField(_("VRTs"),default=False)

    sName = models.CharField(_("Configuracion"), max_length=64,blank=False,null=False)

    sFee = models.PositiveIntegerField(_("TAX"),default=5000,
                help_text=_("Impuesto Tickets ($COP)"),)

    sFeeAmmount = models.PositiveIntegerField(_("$Impuestos"),blank=True,default=0,
                help_text=_("Capital Acumulado en Fee ($COP)"),)

    sDriverPoints = models.PositiveIntegerField(_("Trasporte MinPoints"),default=100,
                help_text=_("$Valor/Punto"),)

    sTickets = models.PositiveIntegerField(_("Tickets"),default=3,
                help_text=_("Tickets/Mensuales"),)

    sTicketsAmmount = models.PositiveIntegerField(_("$TicketsMin"),default=100000,
                help_text=_("Min Volumen x Tickets ($COP)"),)

    gTravelPtsMin = models.PositiveIntegerField(_("VRTs"),blank=False,null=False,default=0,
        help_text=_("% VRT-PTS Minimos"),)

    gTravelName = models.CharField(_("Nombre"), max_length=64,blank=False,null=False,
        help_text=_("Nombre/Referencia del Destino"),)
        
    gTravelBanner = models.ImageField(_("IMG"), upload_to="InvestmentFund/uploads/images/banner/", blank=True, null=True, height_field=None, width_field=None, max_length=128,
        help_text=_("Width 520px x Height 140px"),)
    
    gTravelDate = models.DateTimeField(_("Fecha"), default=datetime(2050, 1, 1),
        help_text=_("Fecha del Sorteo"),)
    
    gWinnerName = models.CharField(_("Ganador"), max_length=32,blank=True)

    IsActive = models.BooleanField(_("Activo"),default=False)


    class Meta:
        verbose_name = _("Configuracion")
        verbose_name_plural = _("Configuraciones")

    def __str__(self):
        return "Configuracion: %s" % (self.pk)
    
class News(models.Model):
        
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(_("Titulo"), max_length=128,blank=True)

    image = models.ImageField(_("Imagen"), upload_to=CustomUpload, height_field=None, width_field=None, max_length=64,
        help_text="Ancho[640px]-Alto[480px]")
    
    description = models.TextField(_("Informacion"),max_length=256,blank=True,null=True)
    date = models.DateTimeField(_("Fecha"), default=timezone.now)


    class Meta:
        verbose_name = _("Noticia")
        verbose_name_plural = _("Noticias")

    def __str__(self):
        return "Noticia: %s" % (self.name)

    
class Associate(models.Model):
    
    pName = models.CharField(_("Empresa"), max_length=32,blank=True)
    pTitle = models.CharField(_("Servicio"), max_length=32,blank=True)
    
    pPtsMin = models.PositiveIntegerField(_("Inversion"),blank=True,null=False,default=0,
        help_text=_("Inversion Minima para Acceder al Beneficio ($COP)"),)
    
    pURL = models.URLField(_("URL"), max_length=128,blank=True,default="https://vrtfund.com/@")
    
    pInfo = models.TextField(_("Texto"), max_length=1024,blank=True,
        help_text=_("Descripcion Principal"),)
    
    pInfoAdd = models.TextField(_("Texto"), max_length=1024,blank=True,
        help_text=_("Informacio Adicional"),)

    pDiscount = models.CharField(_("%"),blank=False,null=False,default="15% OFF", max_length=64,help_text=_("%Descuento/Gratis"),)
      
    pCard = models.ImageField(_("Miniatura"), upload_to="InvestmentFund/uploads/banner/cards/", height_field=None, width_field=None, max_length=128, blank=True, null=True,)
    pBanner = models.ImageField(_("Banner"), upload_to="InvestmentFund/uploads/images/banner/", height_field=None, width_field=None, max_length=128, blank=True, null=True,)

    IsActive = models.BooleanField(_("¿Activo?"),default=True)

    class Meta:
        verbose_name = _("Asociado")
        verbose_name_plural = _("Asociaciones")

    def __str__(self):
        return "Asociado: %s" % (self.pk)

class Schedule(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    username = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name="Usuario")

    driver = models.CharField(_("Conductor"),max_length=64 ,unique=False,
                help_text=_("Codigo del Conductor"))

    date = models.DateTimeField(_("Fecha"), default=timezone.now)

    status = models.CharField(_("Estado"), choices=list_status, default="", max_length=16)

    addres_from = models.CharField(_("Destino"),max_length=64 ,unique=False,null=True,
                help_text=_("Direccion de Origen"))

    addres_to = models.CharField(_("Origen"),max_length=64 ,unique=False,null=True,
                help_text=_("Direccion de Destino"))
    
    distance = models.FloatField(_("Kilometraje"), null=True, blank=True)

    paid = models.PositiveBigIntegerField(_("Valor"),blank=True,default=0,
                help_text=_("$Costo del Servicio"),)


    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("Informacion de Servicios de Transporte")


class Messages(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    full_name = models.CharField(_("Nombre/Apellido"), max_length=64, blank=True)
    email = models.EmailField(_("E-mail"), blank=True)
    date = models.DateTimeField(_("Fecha"), default=timezone.now)
    messages = models.TextField(_("Mensaje"),max_length=256,blank=True,null=True)
    is_view = models.BooleanField(_("¿Visto?"),default=False)

    class Meta:
        verbose_name = _("Mensaje")
        verbose_name_plural = _("Mensajes")

    def __str__(self):
        return "%s" % (self.full_name)