from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:pk>/', Item_Detail_View.as_view(), name='item_detail_view'),
    path('search/', Item_Search_View.as_view(), name='item_search'),
    path('search2/', Item_Search2_View.as_view(), name='item_search2'),
    path('add_item/', login_required(ItemCreate.as_view()), name='add_item'),
    path('my_items/<int:pk>/', login_required(MyItems.as_view()), name='my_items'),
    path('by_category/<int:category_id>/', ViewByCategory.as_view(), name='by_category'),
    path('item_delete/<int:pk>/', login_required(ItemDeleteView.as_view()), name='item_delete'),
    path('item_update/<int:pk>/', login_required(Item_Update_View.as_view()), name='item_update'),
    path('image_delete/<int:pk>/', login_required(Image_Delete_Gallery.as_view()), name='image_delete'),
    path('add_gallery/<int:item_id>/', login_required(AddGalleryView.as_view()), name='add_gallery'),
    path('next_item/<int:item_id>/', Next_ItemView.as_view(), name='next_item'),
    path('prev_item/<int:item_id>/', Prev_ItemView.as_view(), name='prev_item'),
    path('save_item/', create_save_item, name='save_item'),
    path('delete_save_item/', delete_save_item, name='del_save_item'),
    path('saved_items/', login_required(SavedItems_View.as_view()), name='saved_items'),

]
