
from django.urls import path
from . import views


urlpatterns = [
	path('', views.about, name="home"),
	# User Auth
	path('signup/', views.signup, name="signup"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('forgotPassword/', views.forgotPassword, name="forgotPassword"),
	path('resetPassword/<str:id>', views.resetPassword, name="resetPassword"),

    # Menu
	path('about/', views.about, name="about"),
    path('products/', views.products, name="products"),
    path('contact/', views.contact, name="contact"),
	path('activate/<str:id>', views.activateUser, name="activate"),



]