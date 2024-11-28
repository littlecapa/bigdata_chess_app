from django.contrib import admin
from .models import LichessConfigModel, LichessFolderConfigModel, LichessStatusModel, TwicConfigModel, TwicFolderConfigModel, TwicStatusModel

@admin.register(LichessStatusModel)
class LichessStatusModelAdmin(admin.ModelAdmin):
    pass
@admin.register(LichessFolderConfigModel)
class LichessFolderConfigModelAdmin(admin.ModelAdmin):
    pass
@admin.register(LichessConfigModel)
class LichessConfigModelAdmin(admin.ModelAdmin):
    pass
@admin.register(TwicStatusModel)
class LichessStatusModelAdmin(admin.ModelAdmin):
    pass
@admin.register(TwicFolderConfigModel)
class LichessFolderConfigModelAdmin(admin.ModelAdmin):
    pass
@admin.register(TwicConfigModel)
class LichessConfigModelAdmin(admin.ModelAdmin):
    pass