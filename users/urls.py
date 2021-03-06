from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.buy, name = 'buy'),
	path('register/', views.register, name = 'register'),
	path('logout/', views.logout, name = 'logout'),
	path('profile/',views.profile, name = 'profile'),
	path('profile/remove/<int:it>', views.delitem, name = 'delitem'),
	path('profile/<str:message>',views.profile, name = 'profile'),
	path('additem/', views.additem, name = 'additem'),
	path('buy/', views.buy, name = 'buy'),
	path('buy/<str:message>', views.buy, name = 'buy'),
	path('buy/item/<int:it>', views.viewitem, name = 'viewitem'),
	path('catbuy/<str:cat>', views.categorybuy, name = 'catbuy'),
	path('aboutus/', views.aboutus, name = 'aboutus'),
	path('results/', views.search, name = 'search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
