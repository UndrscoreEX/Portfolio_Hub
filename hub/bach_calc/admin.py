from django.contrib import admin
from .models import Height_groups, Age_ref, Income_groups


# admin.site.register(Height_groups)
# admin.site.register(Age_ref)
# admin.site.register(Income_groups)


@admin.register(Height_groups)
class Height_class(admin.ModelAdmin):
    list_display = ['height_cm','ht_per']

    
@admin.register(Age_ref)
class Age_class(admin.ModelAdmin):
    list_display = ['age']


@admin.register(Income_groups)
class Income_class(admin.ModelAdmin):
    list_display = ['age_group','income_yr', 'income_ratio']

