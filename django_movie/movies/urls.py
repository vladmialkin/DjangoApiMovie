from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.MovieListView.as_view(), name='movies_list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/', views.ReviewCreateView.as_view(), name='create_review'),
    path("rating/", views.AddStarRatingView.as_view()),
    path("actors/", views.ActorsListView.as_view(), name='actors_list'),
    path("actors/<int:pk>/", views.ActorDetailView.as_view(), name='actor_detail'),
]

