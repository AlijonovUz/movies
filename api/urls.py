from rest_framework import routers

from .views import GenreViewSet, CountryViewSet, MovieViewSet

router = routers.DefaultRouter()

router.register('genre', GenreViewSet)
router.register('country', CountryViewSet)
router.register('movie', MovieViewSet)

urlpatterns = router.urls