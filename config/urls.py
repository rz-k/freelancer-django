from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('', include('freelancer.account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('pay/', include('freelancer.payment.urls', namespace='pay')),
    path('project/', include('freelancer.project.urls', namespace='project')),
    path('faq/', include('freelancer.faq.urls', namespace='faq')),
    path("api/v1/", include("freelancer.api.urls", namespace="api")),

    # Api Schema
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/redoc/',SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
