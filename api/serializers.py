from rest_framework import serializers
from django.utils.text import slugify

from .models import Genre, Country, Movie, MovieURL


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'slug': {
                'required': False,
                'allow_blank': True
            }
        }

    def validate(self, attrs):
        if not attrs.get('slug'):
            attrs['slug'] = slugify(attrs['name'])
        return attrs


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'slug': {
                'required': False,
                'allow_blank': True
            }
        }

    def validate(self, attrs):
        if not attrs.get('slug'):
            attrs['slug'] = slugify(attrs['name'])
        return attrs


class MovieURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieURL
        fields = ['title', 'type', 'part', 'embed_url']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id', 'like', 'dislike', 'view']
        extra_kwargs = {
            'slug': {
                'required': False,
                'allow_blank': True
            }
        }

    def validate(self, attrs):
        if not attrs.get('slug'):
            attrs['slug'] = slugify(attrs['title'])
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['country'] = CountrySerializer(instance.country).data
        data['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        data['video_items'] = MovieURLSerializer(instance.movie_url.all(), many=True).data

        return data