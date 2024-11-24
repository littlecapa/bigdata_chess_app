from django.contrib import admin
from .models import LichessConfigModel, LichessFolderConfigModel, LichessStatusModel

@admin.register(LichessStatusModel)
class LichessStatusModelAdmin(admin.ModelAdmin):
    pass
@admin.register(LichessFolderConfigModel)
class LichessFolderConfigModelAdmin(admin.ModelAdmin):
    pass
@admin.register(LichessConfigModel)
class LichessConfigModelAdmin(admin.ModelAdmin):
    pass
