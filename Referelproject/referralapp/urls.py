from django.urls import path
from.views import UserRegistration,LoginAPI,UserDetails,ReferralUserSerializer
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
     path('login/', LoginAPI.as_view(), name='user-login'),
      path('userdetails/', UserDetails.as_view(), name='user-details'),
    path('referalusers/', ReferralUserSerializer.as_view(), name='user-refererals'),

]