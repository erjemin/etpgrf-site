from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.index, name='index'),
    path(route='process/', view=views.process_text, name='process_text'),
]
