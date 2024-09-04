from django.contrib import admin

from .models import New_Listing,New_Bid,New_Comment,WatchList
# Register your models here.

admin.site.register(New_Listing)
admin.site.register(New_Bid)
admin.site.register(New_Comment)
admin.site.register(WatchList)

