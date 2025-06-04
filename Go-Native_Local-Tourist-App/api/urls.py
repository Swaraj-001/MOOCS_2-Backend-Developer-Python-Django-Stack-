from django.urls import path, include
from . import views
from .karad_explorer import karad_explorer_urls

urlpatterns = [
    path('', views.landing),


    path('search/', views.search),


    path('city/<str:id>', views.city),

    path('load-location/<str:id>', views.loadLocation),
    path('location/<str:locId>/<str:userId>', views.location),

    path('karad-explorer/', include(karad_explorer_urls)),
]
