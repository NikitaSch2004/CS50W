from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing_new", views.new_listing, name="new_listing"),
    path("<str:user>/watchlist",views.watchlist,name="watchlist"),
    path("categories",views.categories,name="categories"),
    path("category/<str:ctg>",views.category,name="category"),
    path("listing/<str:listing_name>",views.listing,name="listing")
]
