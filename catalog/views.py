from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product, Contact
from .forms import ProductForm, VersionForm
from .services import get_categories


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = get_categories()
        products = [product for product in Product.objects.all() if product.is_published][:6]

        for product in products:
            product.active_version = product.versions.filter(is_active=True).first()

        context['products'] = products
        context['categories'] = categories
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
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
        new_product.owner = self.request.user
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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = 'product'
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        product = get_object_or_404(Product, name=name)
        if product.owner != self.request.user and not self.request.user.is_staff:
            raise Http404

        return product

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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        product = get_object_or_404(Product, name=name)
        if product.owner != self.request.user:
            raise Http404

        return product


class ContactDetailView(ListView):
    model = Contact
    template_name = 'catalog/contacts.html'
    context_object_name = 'contact'
