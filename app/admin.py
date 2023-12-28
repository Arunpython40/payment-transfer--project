from django.contrib import admin
from .models import *

admin.site.register(UserWallet)
admin.site.register(Transaction)