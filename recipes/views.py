from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Recipe, Comment, Rating
from .forms import RecipeForm, CommentForm, RatingForm, UserRegistrationForm


def home(request):
    featured_recipes = Recipe.objects.all().order_by('-created_at')[:3]
    return render(request, 'recipes/home.html', {'featured_recipes': featured_recipes})


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']
    paginate_by = 6


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['rating_form'] = RatingForm()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_url = reverse_lazy('recipes:recipe_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Recipe created successfully!')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(request, 'Please correct the errors below.')
            return self.form_invalid(form)


@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('recipes:recipe_detail', pk=pk)


@login_required
def add_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'value': form.cleaned_data['value']}
            )
            if not created:
                rating.value = form.cleaned_data['value']
                rating.save()
            messages.success(request, 'Rating added successfully!')
    return redirect('recipes:recipe_detail', pk=pk)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'recipes/register.html', {'form': form})


def about(request):
    return render(request, 'recipes/about.html')
