from django.conf.urls import include, url
from django.contrib.auth.views import logout
from accounts import views


urlpatterns = [
    url(r"^send_login_email$", views.send_login_email, name="send_login_mail"),
    url(r"^login$", views.login, name="login"),
    url(r"^logout$", logout, {"next_page": "/"}, name="logout"),
]
