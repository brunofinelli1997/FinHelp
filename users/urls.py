from django.urls import path
from users import views

#Urls User
urlpatterns = [
	path('create/', views.create_user, name='create-user'),
	path('update/<int:pk>', views.update_user, name='update_user'),
]
