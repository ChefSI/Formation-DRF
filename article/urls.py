from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)
router.register("users", UserViewSet, basename="users")
urlpatterns = router.urls