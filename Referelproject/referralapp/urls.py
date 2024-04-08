from django.urls import path
from.views import UserRegistration,LoginAPI,UserDetails,ReferralsEndpoint
urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
     path('login/', LoginAPI.as_view(), name='user-login'),
      path('userdetails/', UserDetails.as_view(), name='user-details'),
    path('referalusers/', ReferralsEndpoint.as_view(), name='user-refererals'),

]
