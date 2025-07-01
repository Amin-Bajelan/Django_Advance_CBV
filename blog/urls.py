from django.urls import path,include
from . import views
from django.views.generic import TemplateView, RedirectView

app_name = 'blog'

urlpatterns = [
    path('index/', views.index, name='home'),
    path('list/', views.ListPost.as_view(), name='about'),
    path('test/', TemplateView.as_view(template_name="blog/test.html",extra_context={"name":"bajelan"}), name='post'),
    path('list-profile/', views.ListProfile.as_view(), name='profile'),
    # path('google/',RedirectView.as_view(url='https://www.google.com'),name='google'),
    path('redirect/', views.RedirectToGoogle.as_view(), name='redirect'),
    path('deatail/<int:pk>/',views.DetailPost.as_view(), name='detail'),
    path('createpost/', views.CreatePost.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', views.EditPost.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='delete_post'),
    path('postapi/', views.api_post_list, name='api-post-list'),
    path('api/v1/', include('blog.api.v1.urls'))
]