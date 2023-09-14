from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product, Contact
from .forms import ProductForm, VersionForm


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()[:6]
        for product in products:
            product.active_version = product.versions.filter(is_active=True).first()
        context['products'] = products
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormSet = formset_factory(VersionForm, extra=1)
        context['version_formset'] = VersionFormSet()
        return context

    def form_valid(self, form):
        new_product = form.save()
        new_product.save()
        selected_version = form.cleaned_data['version']
        selected_version.products.add(new_product)
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Product, name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        product.active_version = product.versions.filter(is_active=True).first()
        context['product'] = product
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product'
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Product, name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormSet = formset_factory(VersionForm, extra=1)
        context['version_formset'] = VersionFormSet()
        return context

    def form_valid(self, form):
        new_product = form.save()
        new_product.save()
        selected_version = form.cleaned_data['version']
        for version in new_product.versions.exclude(pk=selected_version.pk):
            version.products.remove(new_product)
        selected_version.products.add(new_product)
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return get_object_or_404(Product, name=name)


class ContactDetailView(ListView):
    model = Contact
    template_name = 'catalog/contacts.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.kwargs.get('name')
        product = get_object_or_404(Product, name=name)
        product.active_version = product.versions.filter(is_active=True).first()
        context['product'] = product
        return context
