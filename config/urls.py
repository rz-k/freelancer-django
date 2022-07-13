from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [


    path('', include('freelancer.account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('job/', include('freelancer.job.urls', namespace='job')),
    path('pay/', include('freelancer.payment.urls', namespace='pay')),
    path('project/', include('freelancer.project.urls', namespace='project')),
    path('faq/', include('freelancer.faq.urls', namespace='faq')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

