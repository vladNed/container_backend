from users import views
from django.urls import path

app_name = 'users'
urlpatterns = [
    path('users/', views.ContainerUserList.as_view(), name='users-list'),
    path('users/', views.ContainerUserRetrieve.as_view(), name='user-get'),
    path('create-user/', views.ContainerUserCreate.as_view(), name='users-create'),
    path('update-user/', views.ContainerUserUpdate.as_view(), name='user-update'),
    path('update-user/<int:pk>/', views.ContainerUserUpdate.as_view(), name='users-update'),
    path('delete-user/<int:pk>/', views.ContainerUserDestroy.as_view(), name='delete-user')
]
