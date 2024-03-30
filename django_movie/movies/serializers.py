from rest_framework import serializers

from .models import *


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    class Meta:
        model = Movie
        fields = ("title", "tagline")


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    # добавление сериализатора для полей
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Movie
        # Вывод всех полей, исключая введенное
        exclude = ("draft",)
