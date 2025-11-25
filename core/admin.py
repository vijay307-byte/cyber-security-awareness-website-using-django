from django.contrib import admin
from .models import Regi, Images
# Register your models here.
admin.site.register(Regi)
admin.site.register(Images)


admin.site.site_header = "CyberDeck Admin"
admin.site.site_title = "CyberDeck Portal"
admin.site.index_title = "Welcome to the CyberDeck Control Panel"
