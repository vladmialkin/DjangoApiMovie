from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, Actor
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip
from django.db import models
from rest_framework import generics


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Case(models.When(rating__ip=get_client_ip(request), then=True),
                                    default=False, output_field=models.BooleanField()), ).annotate(
            middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('rating'))
        )
        # movies = Movie.objects.filter(draft=False).annotate(
        #     rating_user=models.Count("rating", filter=models.Q(rating__ip=get_client_ip(request))))
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Отзыв к фильму"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод деталей актера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer

