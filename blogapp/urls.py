from django.urls import path, include
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView, RegisterView, BlogListByTagView, AdminDashboardView, BlogUpdateView, BlogDeleteView, TagCreateView, TagUpdateView, TagDeleteView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

app_name = 'blogapp'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('register/', RegisterView.as_view(), name='register'),
    path('tag/<str:tag_name>/', BlogListByTagView.as_view(), name='blog_list_by_tag'), 
    #Nuevas URLs para el panel de administración corregidas
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('tag/create/', TagCreateView.as_view(), name='tag_create'),
    path('tag/<int:pk>/edit/', TagUpdateView.as_view(), name='tag_edit'),
    path('tag/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    #Urls para la autenticación con google
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),  #Rutas para Google
    path('logout/', LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
