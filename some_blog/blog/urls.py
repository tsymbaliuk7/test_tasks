from django.urls import path, include
from .views import CreatePostView, DetailPostView, UpdatePostView, DeletePostView, DeleteAllCommentsView

from django.conf import settings
from django.conf.urls.static import static


app_name = 'blog'
urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create'),
    path('<int:pk>/', DetailPostView.as_view(), name='detail'),
    path('update/<int:pk>/', UpdatePostView.as_view(), name='update'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='delete'),
    path('delete_comments/<int:pk>/', DeleteAllCommentsView.as_view(), name='delete_comments')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
