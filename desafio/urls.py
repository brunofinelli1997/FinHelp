from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

#ADMIN
urlpatterns = [
    #Painel admin
    path('admin/', admin.site.urls),

    #Urls Finhelp
    path('finhelp/', include('finhelp.urls')),
    path('', RedirectView.as_view(url='/finhelp/')),
    path('finhelp/', include('django.contrib.auth.urls')),
    path('finhelp/', include('users.urls')),
]

#STATIC
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)