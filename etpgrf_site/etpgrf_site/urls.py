from django.contrib import admin
from django.urls import path, include
# from etpgrf_site.etpgrf.typograph import Typographer
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('typograph.urls')),
]
