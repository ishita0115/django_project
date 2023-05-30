from app1.views import *
from django.urls import path

urlpatterns = [
    path('first/',first),
    path('login/',login,name='login1'),
    path('register/',register,name='register1'),
    path('table_all/',table_all),
    path('table_filter/',table_filter),
    path('table_all_p/',table_all_p),
    path('table_filter_p/',table_filter_p),
    path('table_get/',table_get),
    path('',index,name='index'),
    path('productcall',productcall,name='productall'),
    path('product-filter/<int:id>/',productcategorywise,name='productfilter1'),
    path('productget1/<int:id>/',singleproduct,name='productget1'),
     
]