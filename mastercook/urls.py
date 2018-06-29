from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('shortcodes/', views.shortcodes)
]

"""
urlpatterns += i18n_patterns(
    path('generic/', include('generic.urls')),
    path('', include('recipes.urls')),
    path('accounts/', include('accounts.urls'))
)
"""

urlpatterns += [
    path('generic/', include('utils.urls')),
    path('', include('recipes.urls')),
    path('accounts/', include('accounts.urls'))
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
