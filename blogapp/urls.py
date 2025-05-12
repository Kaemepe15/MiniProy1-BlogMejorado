from django.urls import path
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView, RegisterView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blogapp'


urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('register/', RegisterView.as_view(), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])