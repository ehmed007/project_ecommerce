from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('view_product/<slug:slug>/',views.view_product, name='view_product'),
    path('category_filter/<slug:slug>/',views.category_filter, name='category_filter'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('view_cart/',views.view_cart, name='view_cart'),
    path('manage_cart/<int:cp_id>/',views.manage_cart, name='manage_cart'),
    path('check_out/',views.check_out, name='checkout'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.customer_login, name='login'),
    path('logout/',views.logout, name='logout'),
]
