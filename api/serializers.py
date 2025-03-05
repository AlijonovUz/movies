from rest_framework import serializers
from django.utils.text import slugify

from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
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


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
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

        data['genre'] = GenreSerializer(instance.genre.all(), many=True).data

        return data
