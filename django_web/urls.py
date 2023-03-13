from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_shop.urls')),
    path('accounts/', include('app_login.urls')),
    path('cart/', include('app_cart.urls')),
    path('payment/', include('payment.urls')),
    path('api/', include('api.urls')),
    ]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)