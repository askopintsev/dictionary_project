from django.urls import path

from . import views


urlpatterns = [
    path("dictionaries/", views.DictionariesView.as_view()),
    path("elements/", views.ElementsView.as_view()),
    ]
