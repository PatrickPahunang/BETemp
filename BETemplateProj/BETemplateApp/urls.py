
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.landing, name='landing'),
    path('users/create/', views.create_user, name='create_user'),
    path('api/example/', views.api_example, name='api-example'),
    path('login/api/', views.login_api, name='login_api'),
    path('update/api/', views.update_user, name='update_user'),
    path('get_user/api/<int:user_id>/', views.get_user, name='get_user'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

