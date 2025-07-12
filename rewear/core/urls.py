# core/urls.py

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    # --- Main Pages ---
    path('', views.home_view, name='home'),
    path('item/<int:pk>/', views.item_detail_view, name='item_detail'),
    path('add/', views.add_item_view, name='add_item'),
    
    # --- The signup URL belongs here because it uses our custom view ---
    path('signup/', views.signup_view, name='signup'),
    # --- Dashboard & Swapping ---
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('request_swap/<int:item_pk>/', views.request_swap_view, name='request_swap'),
    path('accept_swap/<int:swap_pk>/', views.accept_swap_view, name='accept_swap'),
    path('decline_swap/<int:swap_pk>/', views.decline_swap_view, name='decline_swap'),

    path('checkout/<int:item_pk>/', views.checkout_view, name='checkout'),
    path('purchase_success/', views.purchase_success_view, name='purchase_success'),
    
    # The login and logout paths have been REMOVED from this file
]
