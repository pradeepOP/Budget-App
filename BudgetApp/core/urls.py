from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("delete-transaction/<str:pk>/",
         views.delete_transaction, name="delete-transaction"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("signup/", views.signupView, name="signup"),
    path("transactions/", views.transactionView, name="transactions"),
    path("charts/", views.chartView, name="charts"),
]
