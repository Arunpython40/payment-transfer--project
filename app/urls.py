from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_page , name='login'),
    path('logout',views.logout_page,name="logout"),
    path('register', views.register, name='register'),
    path('verify', views.verifiy, name='verify'),
    path('pay/<int:id>/', views.pay, name='pay'),
    path('success', views.success, name='success'),
    path('pin', views.pinchange, name='pin'),
    path('phonechange', views.phonechange, name='phonechange'),
    path('passchange', views.passchange, name='passchange'),
    
    
]
