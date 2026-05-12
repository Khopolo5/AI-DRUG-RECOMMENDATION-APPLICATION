from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name = "home")
    path("", views.base, name="base"),
    path("history/", views.history, name = "history"),
    # path("predict/", views.predict_condition, name="predict")

]