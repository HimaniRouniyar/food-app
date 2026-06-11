
from . import views
from django.urls import path
# from django.views.decorators.cache import cache_page
app_name = 'myapp'

urlpatterns = [
    path("",views.index,name='index'),
    #  path("",cache_page(60 * 15) (views.index),name='index'),
    path("<int:id>",views.detail,name='detail'),
    path('add/', views.ItemCreateView.as_view(),name='create_item'),
    path('edit/<int:pk>',views.UpdateItem.as_view(),name='edit_item'),
    path('delete/<int:pk>',views.DeleteItem.as_view(),name='delete_item'),
]
