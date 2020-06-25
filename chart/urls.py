# chart/urls.py
from django.contrib import admin
from django.urls import path
from chart import views                                     # !!!

urlpatterns = [
    path('', views.home, name='home'),
    path('ticket-class/',
         views.ticket_class_view, name='ticket_class_view'),
    path('world-population/',
         views.world_population, name='world_population'),  # !!!
    path('covid_cases/',
         views.covid_cases, name='covid_cases'),
    path('covid_cases_per_capita/',
         views.covid_cases_per_capita, name='covid_cases_per_capita'),
    path('admin/', admin.site.urls),
]
