from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(vendor_register)


admin.site.register(Vendor_profile)
admin.site.register(State_name)

admin.site.register(Product_categories)
admin.site.register(Upload_product)
