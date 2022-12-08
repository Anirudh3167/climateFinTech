from django.contrib import admin
from .models import *
# Register your models here.

# Basic Platform models
admin.site.register(User_Details)
admin.site.register(HelpDesk)

# Fin Tech models
admin.site.register(Transactions)

# Store Models
admin.site.register(CartItems)
admin.site.register(Products)
admin.site.register(Lables)

# CLimate Tech Models
admin.site.register(records)

# Blog models
admin.site.register(Blogs)
