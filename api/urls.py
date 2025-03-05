from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register('genres', GenreViewSet)
router.register('movies', MovieViewSet)

urlpatterns = router.urls