from django.urls import path
from django.conf.urls.static import static

from . import views
from .base_config import WORKSPACE_DIR

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:path_url>', views.index, name='index'),
    path('video_extract/<str:path_url>', views.video_extract, name='video_extract'),
    path('model_train/<str:path_url>', views.model_train, name='model_train'),
    path('video_merge/<str:path_url>', views.video_merge, name='video_merge'),
    path('photo_src/<str:path_url>', views.photo_src, name='photo_src'),

    # второстепенные урлы
    path('create_workspace/new', views.create_workspace, name='create_workspace'),
    ]

urlpatterns += static('/workspace/', document_root=f'{WORKSPACE_DIR}')
