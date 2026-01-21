from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path(route='adm-in/', view=admin.site.urls),
    path(route='', view=include('typograph.urls')),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # runserver автоматически раздает статику из STATICFILES_DIRS,
    # поэтому добавлять static(settings.STATIC_URL...) НЕ НУЖНО.
    # Это только ломает путь, направляя его в STATIC_ROOT.
    
    # А вот медиа runserver не раздает, поэтому это нужно:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
