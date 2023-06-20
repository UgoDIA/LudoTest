from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# router.register('Members',MembersViewset, basename='Members')
router.register('JeuViewset',JeuViewset, basename='JeuViewset')
router.register('EditeurViewset',EditeurViewset, basename='EditeurViewset')
router.register('JeuEditeur', JoinedViewSet)

urlpatterns = router.urls