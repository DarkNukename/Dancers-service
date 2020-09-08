from django.urls import path
from .views.couples_view import CouplesView, CoupleView
from .views.dancers_view import DancersView, DancerView

urlpatterns = [
    path('sportsmans/', DancersView.as_view()),
    path('sportsman/<uuid:uuid>/', DancerView.as_view()),
    path('couples/', CouplesView.as_view()),
    path('couple/<uuid:uuid>/', CoupleView.as_view())
]