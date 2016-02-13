from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$','QA.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    #    url(r'^accounts/', include('registration.backends.simple.urls')), # not sure
	#url(r'^$', 'django.contrib.auth.views.login'),
    # url(r'^logout/$', logout_page),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    # url(r'^register/$', register),
    # url(r'^register/success/$', register_success),
]
