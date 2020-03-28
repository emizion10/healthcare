from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from .models import *



class AccountAdmin(UserAdmin):
	list_display = ('username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('username',)
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(MyUser, AccountAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(MedicalRecord)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Preference)
admin.site.register(Comments)










