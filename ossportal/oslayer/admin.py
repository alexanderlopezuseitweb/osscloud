from django.contrib import admin

from .models import User
from .models import AccessLevel
from .models import Company
from .models import Setting
from .models import Country
from .models import State
from .models import City
from .models import Group


# Register your models here.

admin.site.register(User)
admin.site.register(AccessLevel)
admin.site.register(Company)
admin.site.register(Setting)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Group)
