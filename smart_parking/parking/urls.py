from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('slots/', views.slots_view, name='slots'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('enter_verification_code/<int:slot_id>/', views.enter_verification_code, name='enter_verification_code'),
    path('release/<int:booking_id>/', views.release_slot, name='release_slot'),

    path('history/', views.history_view, name='history'),
    path('account/', views.account_view, name='account'),
    path('check-parking/', views.check_parking, name='check_parking'),
    path("update-slots/", views.update_parking_slots, name="update_slots"),
]
