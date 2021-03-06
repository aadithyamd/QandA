from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login, logout
import QA.views
urlpatterns = [
    # Examples:
    url(r'^$',QA.views.home, name='home'),
    url(r'^write/$',QA.views.listquestions, name='write'),
    url(r'^admin/', include(admin.site.urls),name='admin'),
    url(r'^accounts/login/$',login),
    url(r'^accounts/profile/$',QA.views.home, name='home'),
    url(r'^accounts/logout/$', logout),
    url(r'^register/$',QA.views.register_view ,name='register'),
    url(r'^write/(?P<question_id>[0-9]*)$',QA.views.detail ,name='question_id'), ##
    url(r'^logout/',QA.views.logout_view, name='logout'),
    url(r'^read/$', QA.views.read ,name='read'),
    url(r'^search/$',QA.views.search,name='search'),
    url(r'^about/$',QA.views.about,name='about'),
    url(r'^report/$',QA.views.report,name='report'),
    url(r'^password/$',QA.views.password_change,name='password'),
    url(r'^success/$',QA.views.success,name='success'),
    url(r'^categories/(?P<category_id>[0-9]*)$',QA.views.category,name='category'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
