from django.urls import path
from . import views

urlpatterns = [
    path('StoneCharges/', views.homePage, name='generate-file-ChargesCounts_MainPage'),
    path('StoneCharges/Morning', views.StoneMorningCounts, name='generate-file-ChargesCounts_MorningPage'),
    path('StoneCharges/Evening', views.StoneEveningCounts, name='generate-file-ChargesCounts_MorningPage'),
    path('generate-file-ChargesCounts', views.generate_file_ChargesCounts, name='generate_file_ChargesCounts'),
]
