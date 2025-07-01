from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', views.PostModelViewSet, basename='PostViewSet')
router.register('category', views.CategoryModelViewSet, basename='category')

app_name = 'api-v1'

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    # path('post/', views.PostList, name='Post_List'),
    # path('post/<int:id>/', views.PostDetail, name='Post_Detail'),
    # path('post/', views.PostList.as_view(), name='Post_List'),
    # path('post/<int:pk>/', views.PostDetail.as_view(), name='Post_Detail'),
    path('', include(router.urls)),
]
