from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class DataStore(models.Model):

    coin_id = models.CharField(_('Coin Id'), max_length=10)
    coin_name = models.CharField(_('Coin Name'), max_length=225)
    current_price = models.DecimalField(_('Current Price'), decimal_places=4, max_digits=20)
    cdate = models.DateTimeField(_('Created Date'), auto_now_add=True)
    last_updated = models.DateTimeField(_('Last Updated'))
    is_active = models.BooleanField(_('Is Active'), default=True)
    
    class Meta:
        verbose_name = _("DataStore")
        verbose_name_plural = _("DataStores")
        ordering = ['-cdate']

    def __str__(self):
        return f"{self.coin_id}:{self.coin_name}:{str(self.current_price)}"
