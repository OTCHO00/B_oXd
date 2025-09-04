from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("series/", views.serie),
    path("add/", views.film_form_view.as_view()),
    path("add_serie/", views.serie_form_view.as_view()),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('update_order/', views.update_order, name='update_order'),
    path('update_order_serie/', views.update_order_serie, name='update_order'),
    path('search-movies/', views.search_movies, name='search_movies'),
    path('get-movie-details/<int:movie_id>/', views.get_movie_details, name='get_movie_details'),
    path('search-series/', views.search_series, name='search_series'),
    path('get-serie-details/<int:serie_id>/', views.get_serie_details, name='get_serie_details'),
]