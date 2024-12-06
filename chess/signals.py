from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LichessConfigModel, LichessStatusModel, LichessFolderConfigModel, TwicConfigModel, TwicFolderConfigModel, TwicStatusModel

from .proxies.twic_proxy import TwicProxy
from .proxies.li_proxy import LiProxy

def refresh_TwicProxy():
    twic_proxy = TwicProxy()
    twic_proxy.refresh()

def refresh_LiProxy():
    print("Refresher")
    li_proxy = LiProxy()
    li_proxy.refresh()

@receiver(post_save, sender=(LichessConfigModel, LichessStatusModel, LichessFolderConfigModel))
def after_li_update(sender, instance, created, **kwargs):
    refresh_LiProxy()

@receiver(post_save, sender=(TwicConfigModel, TwicFolderConfigModel, TwicStatusModel))
def after_twic_update(sender, instance, created, **kwargs):
    refresh_TwicProxy()