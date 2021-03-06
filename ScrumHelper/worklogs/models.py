from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone




class Worklog(models.Model):
    '''
    Worklog object's class
    '''
    log_date = models.DateTimeField(_("log date"), default=timezone.now)
    logged_hour = models.IntegerField(_("logged hours"))
    log_user = models.ForeignKey("users.Profile", verbose_name=_(""), on_delete=models.CASCADE, null=True)
    

    class Meta:
        verbose_name = _("worklog")
        verbose_name_plural = _("worklogs")



