from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from accounts.views import ( CustomUserList, CustomUserCreate, CustomUserDetail, CustomUserUpdate, 
CustomUserDelete)
    

urlpatterns = [
    
    #path('activate/', activate, name="activate"), 
    
    #path('register/', register, name="register"), 
    #path('login_user/', login_user, name="login"), 
    #path('logout_user/', logout_user, name="logout"), 
    #path('change_password/', change_password, name="change_password"), 
   

    #path('all_usuarios/', UserList.as_view(), name='all_usuarios'),
    path('all_users/', CustomUserList.as_view(), name='all_users'),
    path('new_user/', CustomUserCreate.as_view(), name='user_create'),
    path('detail_user/<int:pk>/', CustomUserDetail.as_view(), name='user_detail'),
    path('update_user/<int:pk>/', CustomUserUpdate.as_view(), name='user_update'),
    path('delete_user/<int:pk>/', CustomUserDelete.as_view(), name='user_delete'), 

]
  