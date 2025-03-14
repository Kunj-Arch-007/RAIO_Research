from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.homePage), 

    # Navigation Bar 

    # DailyCharges URLs
    path('DailyCharges/', views.dailyChargesPage, name="daily_charges"), 
    path('DailyCharges/cmc', views.cmc_dailychargesRenderFile, name="cmc_daily_charges"), 
    path('DailyCharges/coolkidz', views.coolkidz_dailychargesRenderFile, name="coolkidz_daily_charges"),
    path('DailyCharges/Gastro', views.GastroenterologyAtlanta_dailyChargesRenderFile, name="gastro_daily_charges"), 
    path('DailyCharges/Gwinnett', views.Gwinnett_dailyChargesRenderFile, name="gwinnett_daily_charges"), 
    path('DailyCharges/Gulf', views.Gulf_dailyChargesRenderFile, name="gulf_daily_charges"), 
    path('DailyCharges/HPC', views.HPC_dailyChargesRenderFile, name="hpc_daily_charges"),
    path('DailyCharges/SMP', views.SMP_dailyChargesRenderFile, name="smp_daily_charges"),
    path('DailyCharges/SWMD', views.SWMD_dailyChargesRenderFile, name="swmd_daily_charges"),
    path('DailyCharges/ShivDhara', views.ShivDhara_dailyChargesRenderFile, name="shivdhara_daily_charges"),
    path('DailyCharges/Thomas', views.Thomas_dailyChargesRenderFile, name="thomas_daily_charges"), 
    path('DailyCharges/Stone', views.Stone_dailyChargesRenderFile, name="stone_daily_charges"), 
    path('DailyCharges/MAG', views.MAG_dailyChargesRenderFile, name="mag_daily_charges"),
    path('DailyCharges/RPL', views.RPL_dailyChargesRenderFile, name="mag_daily_charges"),
    path('DailyCharges/EIM', views.EIM_dailyChargesRenderFile, name="eim_daily_charges"), 

    path('generate-file-dailyCharges', views.generate_file_view_charges, name="generate_daily_charges"),

    # DailyEV URLs
    path('DailyEV/', views.dailyEVPage, name = "dailyEV"), 
    path('DailyEV/CMD', views.CMD_DailyEVRenderFile, name="cmd_daily_ev"), 
    path('DailyEV/HealthFirst', views.HealthFirst_DailyEVRenderFile, name="healthfirst_daily_ev"),
    path('DailyEV/Coolkidz', views.Coolkids_DailyEVRenderFile, name="coolkidz_daily_ev"), 
    path('DailyEV/MAG', views.MAG_DailyEVRenderFile, name="mag_daily_ev"), 
    path('DailyEV/SWMD', views.SWMD_DailyEVRenderFile, name="swmd_daily_ev"), 
    path('DailyEV/BHO', views.BHO_DailyEVRenderFile, name="bho_daily_ev"),

    path('generate-file-dailyEV', views.generate_file_dailyEV, name='generate_daily_ev'), 

    # AR_CLients List URLs
    path('AR_Clients/', views.ARPage, name = "ar_page" ), 
    path('AR_Clients/Coolkidz', views.Coolkidz_ARRenderFile, name="coolkidz_ar"),
    path('AR_Clients/GastroenterologyAtlanta', views.GastroenterologyAtlanta_ARRenderFile, name="gastro_ar"), 
    path('AR_Clients/MAG', views.MAG_ARRenderFile, name="mag_ar"),
    path('AR_Clients/CMD', views.CMD_ARRenderFile, name="cmd_ar"), 
    path('AR_Clients/HPC', views.HPC_ARRenderFile, name="hpc_ar"), 
    path('AR_Clients/SWMD', views.SWMD_ARRenderFile, name="swmd_ar"), 
    path('AR_Clients/Oak_Hills', views.Oak_Hills_ARRenderFile, name="oak_hills_ar"), 
    path("AR_Clients/Gulf", views.Gulf_ARRenderFile, name="gulf_ar"), 

    # Under "AR_CLients"....Action of AR_Process....
    path("AR_Clients/Coolkidz/AR_Process", views.Coolkidz_AR_ProcessRenderFile, name="CoolKidz_AR_Process_File"), 
    path("AR_Clients/Coolkidz/EPD_Process", views.Coolkidz_EPD_ProcessRenderFile, name="CoolKidz_AR_Process_File"), 

    path('generate-file-AR', views.generate_file_AR, name="generate_ar"), 
    path('generate-file-EPD', views.generate_file_EPD, name="generate-epd"), 

    # Log Path
    path('logs/', views.logs_view, name="view_logs")
]
