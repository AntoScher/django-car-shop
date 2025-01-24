"""
URL configuration for car_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:car_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:car_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  #
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)