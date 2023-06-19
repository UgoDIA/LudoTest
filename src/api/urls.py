from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# router.register('Members',MembersViewset, basename='Members')

urlpatterns = router.urls