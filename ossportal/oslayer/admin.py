from django.contrib import admin

from .models import User
from .models import AccessLevel
from .models import Company
from .models import Setting
# Register your models here.

admin.site.register(User)
admin.site.register(AccessLevel)
admin.site.register(Company)
admin.site.register(Setting)