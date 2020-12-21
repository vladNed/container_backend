from projects import views
from rest_framework import routers

app_name = 'projects'
router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')
router.register(r'project-access', views.ProjectUserViewSet, basename='project-access')

urlpatterns = router.urls
