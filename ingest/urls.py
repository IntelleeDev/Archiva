from django.conf.urls import url
from ingest import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # archiva/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # archiva/login/
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # archiva/logout/
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # archiva/signup/
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),

    # archiva/dashboard/main/id=user_id  HOME DASHBOARD VIEW URL
    url(r'^dashboard/main/id=(?P<id>[0-9]+)$', views.MainDashView.as_view(), name='maindash'),

    url(r'^dashboard/home/id=(?P<id>[0-9]+)$', views.HomeDashView.as_view(), name='homedash'),

    # archiva/dashboard/ingest/id=user_id  INGEST DASHBOARD VIEW
    url(r'^dashboard/ingest/id=(?P<id>[0-9]+)$', views.IngestDashView.as_view(), name='ingestdash'),

    # archiva/dashboard/store/id=user_id
    url(r'^dashboard/store/id=(?P<id>[0-9]+)$', views.StoreDashView.as_view(), name='storedash'),

    # archiva/dashboard/search/id=user_id
    url(r'^dashboard/search/id=(?P<id>[0-9]+)$', views.SearchDashView.as_view(), name='searchdash'),

    # End point urls
    url(r'^repository/create/id=(?P<id>[0-9]+)$', views.CreateRepository.as_view(), name='create'),
    url(r'^allusers/$', views.get_all_users, name='allusers'),
    url(r'^content/id=(?P<id>[0-9]+)$', views.get_repository_content, name='content'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)