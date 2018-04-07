"""B2E_Commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from online_shopping_cart import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('adminPanel/', views.admin_panel, name="adminPanel"),
    path('edit_item/<int:id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:id>/', views.delete_item, name='delete_item'),
    path('test/', views.add_cart_item, name="test"),
    path('product_summary/', views.product_summary, name="product_summary"),
    path('remove_cart_item/<int:id>/', views.remove_cart_item, name="remove_cart_item"),
    path('remove_all_cart_items/', views.remove_all_cart_items, name="remove_all_cart_items"),
    path('user_registration/', views.user_registration, name="user_registration"),
    path('add_shipping_info/', views.add_shopping_info, name="add_shopping_info"),
    path('confirm_shipping_info/', views.confirm_shipping_info, name="confirm_shipping_info"),
    path('shipping_history/', views.shipping_history, name="shipping_history"),
    path('approve_payment_status/<int:id>/', views.approve_shipping_info, name="approve_payment_status"),
    path('show_voucher_information/<int:id>/', views.show_voucher_information, name="show_voucher_information"),
    path('update_cart_items/<int:id>/', views.update_cart_items, name="update_cart_items"),
    path('search/', views.search_result, name="search_result"),
    path('login_or_register/', views.login_or_register, name="login_or_register"),
    path('login/', views.user_login, name="user_login"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
