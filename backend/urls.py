from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('admin/', admin.site.urls),
    
    path('userprofile/', include('UserProfile.urls')),
    path('post/', include('blog.urls')),
    path('chat/', include('chat.urls')),
    path('frontend/', TemplateView.as_view(template_name='index.html')),   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)