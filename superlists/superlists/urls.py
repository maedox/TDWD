#from django.conf.urls import patterns, include, url
from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r"^$", "lists.views.home_page", name="home"),
    url(r"^lists/some-list-id/$", "lists.views.view_list", name="view_list"),
    url(r"^lists/new$", "lists.views.new_list", name="new_list"),
    # url(r'^superlists/', include('superlists.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
