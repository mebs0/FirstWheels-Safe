from django.urls import path
from .views import getvehicledata, usergarageapi, userchecklistapi, anprscanner

urlpatterns = [
    # looks up the car
    path('lookup/', getvehicledata, name='lookup_vehicle'),
    # the anpr scanner
    path('scananpr/', anprscanner), 
    # checklist api with post and get 
    path('checklists/', userchecklistapi),
    # garage api with post and get
    path('garage/', usergarageapi),
]
