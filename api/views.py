from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly
from .serializers import *
from .filters import MovieFilter
from .models import *


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    throttle_scope = 'genre'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response({
            'data': response.data,
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MovieFilter
    search_fields = ['name']
    lookup_field = 'slug'
    throttle_scope = 'movie'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response({
            'data': response.data,
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, slug=None):
        movie = self.get_object()
        user = request.user

        reaction, created = MovieReaction.objects.get_or_create(movie=movie, user=user)

        if not created:
            if reaction.reaction == 'like':
                movie.like -= 1
                reaction.delete()
            elif reaction.reaction == 'dislike':
                movie.dislike -= 1
                movie.like += 1
                reaction.reaction = 'like'
                reaction.save()
        else:
            movie.like += 1
            reaction.reaction = 'like'
            reaction.save()

        movie.save()

        return Response({
            'data': {
                'like': int(movie.like),
                'dislike': int(movie.dislike)
            },
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, slug=None):
        movie = self.get_object()
        user = request.user

        reaction, created = MovieReaction.objects.get_or_create(movie=movie, user=user)

        if not created:
            if reaction.reaction == 'dislike':
                movie -= 1
                reaction.delete()
            elif reaction.reaction == 'like':
                movie.like -= 1
                movie.dislike += 1
                reaction.reaction = 'dislike'
                reaction.save()
        else:
            movie.dislike += 1
            reaction.reaction = 'dislike'
            reaction.save()

        movie.save()

        return Response({
            'data': {
                'like': int(movie.like),
                'dislike': int(movie.dislike)
            },
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], permission_classes=[permissions.AllowAny])
    def view(self, request, slug=None):
        movie = self.get_object()

        movie.view += 1
        movie.save()

        return Response({
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)
