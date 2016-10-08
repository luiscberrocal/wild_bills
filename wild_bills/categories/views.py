from braces.views import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import UpdateView, CreateView, DetailView, ListView

from .forms import CategoryForm
from .models import Category


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    context_object_name = 'category'
    form_class = CategoryForm


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    context_object_name = 'category'
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        #context['form'].fields['employee'].queryset = Employee.objects.from_group(self.kwargs['group_slug'])
        return context

    def form_valid(self, form):
        #obj = form.save(commit=False)
        #employee = Employee.objects.get(user=self.request.user)
        #obj.coach = employee
        #obj.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    context_object_name = 'category'


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        qs = super(CategoryListView, self).get_queryset()
        # Filter qs if need be
        return qs