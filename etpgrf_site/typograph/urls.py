from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process_text, name='process_text'),
    path('stats/summary/', views.get_stats_summary, name='stats_summary'),
    path('stats/track-copy/', views.track_copy, name='track_copy'),
]
