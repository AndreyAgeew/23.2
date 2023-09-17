from django.contrib.auth.decorators import login_required
from django.urls import path

from catalog.views import ProductListView, ContactDetailView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = 'catalog'
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactDetailView.as_view(), name='contacts'),
    path('product/create/', login_required(ProductCreateView.as_view()), name='product_create'),
    path('product/<str:name>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<str:name>/update/', login_required(ProductUpdateView.as_view()), name='product_update'),
    path('product/<str:name>/delete/', login_required(ProductDeleteView.as_view()), name='product_delete'),

]
