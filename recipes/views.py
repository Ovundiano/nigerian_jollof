from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Recipe, Comment, Rating
from .forms import RecipeForm, CommentForm, RatingForm, UserRegistrationForm
from django.http import HttpResponseForbidden


def home(request):
    featured_recipes = Recipe.objects.all().order_by('-created_at')[:3]
    return render(request, 'recipes/home.html', {'featured_recipes': featured_recipes})


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/database_recipes.html'  # Use the new template
    context_object_name = 'recipes'
    ordering = ['-created_at']
    paginate_by = 6


def jollof_varieties(request):
    return render(request, 'recipes/recipe_list.html')


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize forms
        context['comment_form'] = CommentForm()
        context['rating_form'] = RatingForm()

        # Get existing rating for the user if logged in
        if self.request.user.is_authenticated:
            existing_rating = Rating.objects.filter(
                recipe=self.object,
                user=self.request.user
            ).first()
            if existing_rating:
                context['rating_form'] = RatingForm(initial={'value': existing_rating.value})

        # Get comments ordered by most recent
        context['comments'] = self.object.comment_set.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to comment or rate.')
            return redirect('login')

        # Handle comment submission
        if 'content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = self.object
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added successfully!')

        # Handle rating submission
        if 'value' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating, created = Rating.objects.get_or_create(
                    recipe=self.object,
                    user=request.user,
                    defaults={'value': rating_form.cleaned_data['value']}
                )
                if not created:
                    rating.value = rating_form.cleaned_data['value']
                    rating.save()
                messages.success(request, 'Rating updated successfully!')

        return redirect('recipes:recipe_detail', pk=self.object.pk)


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


def jollof_varieties(request):
    return render(request, 'recipes/recipe_list.html')


def variety_detail(request, variety):
    varieties_info = {
        'smoky': {
            'title': 'Smoky Jollof',
            'description': 'The signature smoky flavor that Nigerian Jollof is famous for.',
            'cooking_time': '1 hour 30 minutes',
            'difficulty': 'Medium',
            'ingredients': [
                '2 cups long-grain rice',
                '4 large tomatoes',
                '2 red bell peppers',
                '2 scotch bonnet peppers',
                'Vegetable oil',
                'Seasonings and spices'
            ],
            'instructions': [
                'Blend tomatoes, peppers, and onions',
                'Parboil rice and rinse',
                'Cook tomato sauce until reduced',
                'Combine rice and sauce',
                'Cook on low heat for smoky flavor'
            ]
        },
        'firewood': {
            'title': 'Firewood Jollof',
            'description': 'Traditional firewood-cooked Jollof with authentic woody aroma.',
            'cooking_time': '2 hours',
            'difficulty': 'Hard',
            'ingredients': [
                '3 cups long-grain rice',
                '6 large tomatoes',
                '3 red bell peppers',
                '3 scotch bonnet peppers',
                'Palm oil',
                'Traditional seasonings'
            ],
            'instructions': [
                'Prepare firewood or charcoal',
                'Blend ingredients for sauce',
                'Cook sauce in cast iron pot',
                'Add rice and cook slowly',
                'Allow smoke to infuse flavor'
            ]
        },
        'party': {
            'title': 'Party Jollof',
            'description': 'The celebratory version served at Nigerian parties and gatherings.',
            'cooking_time': '2 hours 30 minutes',
            'difficulty': 'Medium',
            'ingredients': [
                '5 cups long-grain rice',
                '8 large tomatoes',
                '4 red bell peppers',
                '3-4 scotch bonnet peppers',
                'Vegetable oil',
                'Chicken stock',
                'Bay leaves',
                'Thyme, curry powder, and other seasonings'
            ],
            'instructions': [
                'Prepare large pot or dutch oven',
                'Blend tomatoes, peppers, and onions',
                'Fry blended mixture until reduced by half',
                'Parboil rice and rinse thoroughly',
                'Layer seasoned sauce and rice',
                'Cover tightly and cook on low heat',
                'Let rest before serving to large crowd'
            ]
        },
        'native': {
            'title': 'Native Jollof',
            'description': 'Traditional village-style preparation with local ingredients.',
            'cooking_time': '2 hours',
            'difficulty': 'Medium-Hard',
            'ingredients': [
                '3 cups local rice (not parboiled)',
                'Fresh tomatoes and peppers',
                'Palm oil',
                'Locust beans (iru)',
                'Smoked fish or dried crayfish',
                'Native spices and herbs'
            ],
            'instructions': [
                'Prepare traditional clay pot if available',
                'Pound or grind fresh tomatoes and peppers',
                'Heat palm oil in pot until clear',
                'Add blended mixture and cook until raw smell disappears',
                'Add cleaned rice without parboiling',
                'Add traditional seasonings and smoked ingredients',
                'Cook on wood fire if possible for authentic taste'
            ]
        },
        'quick': {
            'title': 'Quick Jollof',
            'description': 'A faster preparation that maintains authentic flavor.',
            'cooking_time': '45 minutes',
            'difficulty': 'Easy',
            'ingredients': [
                '2 cups parboiled rice',
                '1 can tomato paste',
                '1 onion, chopped',
                '1 bell pepper, chopped',
                '1-2 scotch bonnet peppers (to taste)',
                'Vegetable oil',
                'Stock cube and seasonings'
            ],
            'instructions': [
                'Heat oil and sauté onions',
                'Add tomato paste and fry for 2-3 minutes',
                'Add chopped peppers and seasonings',
                'Pour in 2.5 cups of water or stock',
                'Add rice and stir well',
                'Cover and cook on medium-low heat for 25-30 minutes',
                'Let rest for 5 minutes before serving'
            ]
        },
        'coconut': {
            'title': 'Coconut Jollof',
            'description': 'A coastal twist with coconut milk adding richness and depth.',
            'cooking_time': '1 hour 15 minutes',
            'difficulty': 'Medium',
            'ingredients': [
                '2 cups long-grain rice',
                '1 can coconut milk',
                '3 large tomatoes',
                '2 red bell peppers',
                '1-2 scotch bonnet peppers',
                'Coconut oil',
                'Fresh thyme and bay leaves',
                'Stock cube and seasonings'
            ],
            'instructions': [
                'Blend tomatoes, peppers, and onions',
                'Heat coconut oil and fry blended mixture',
                'Add coconut milk and bring to simmer',
                'Add washed rice and additional water if needed',
                'Add herbs and seasonings',
                'Cover and cook on low heat until rice is tender',
                'Garnish with fresh herbs or toasted coconut flakes'
            ]
        }
    }

    variety_data = varieties_info.get(variety)
    if not variety_data:
        return redirect('recipes:jollof_varieties')

    return render(request, 'recipes/variety_detail.html', {
        'variety': variety,
        'recipe': variety_data
    })


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user is the comment author
    if comment.user != request.user:
        return HttpResponseForbidden("You cannot edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('recipes:recipe_detail', pk=comment.recipe.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'recipes/edit_comment.html', {
        'form': form,
        'comment': comment
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user is the comment author
    if comment.user != request.user:
        return HttpResponseForbidden("You cannot delete this comment.")

    recipe_id = comment.recipe.id
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('recipes:recipe_detail', pk=recipe_id)

    return render(request, 'recipes/delete_comment_confirm.html', {
        'comment': comment
    })
