# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Comment, Rating
from .forms import RecipeForm, CommentForm, RatingForm, UserRegistrationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category


class HomePageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )

        # Create some test recipes
        for i in range(5):
            Recipe.objects.create(
                title=f"Test Recipe {i}",
                description=f"Description for test recipe {i}",
                ingredients=f"Ingredients for test recipe {i}",
                instructions=f"Instructions for test recipe {i}",
                cooking_time=30,
                servings=4,  # Added servings field
                difficulty="Easy",
                author=self.user,
            )

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "recipes/home.html")

    def test_home_page_contains_featured_recipes(self):
        response = self.client.get("/")
        self.assertTrue("featured_recipes" in response.context)
        self.assertEqual(
            len(response.context["featured_recipes"]), 3
        )  # Checking if 3 featured recipes are displayed


class RecipeListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )

        # Create some test recipes
        for i in range(10):
            Recipe.objects.create(
                title=f"Test Recipe {i}",
                description=f"Description for test recipe {i}",
                ingredients=f"Ingredients for test recipe {i}",
                instructions=f"Instructions for test recipe {i}",
                cooking_time=30,
                servings=4,
                difficulty="Easy",
                author=self.user,
            )

    def test_recipe_list_view_status_code(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_view_template(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertTemplateUsed(response, "recipes/database_recipes.html")

    def test_recipe_list_pagination(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            len(response.context["recipes"]), 6
        )  # Check if 6 recipes are displayed per page


class RecipeDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.client = Client()

        # Create a test recipe
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            ingredients="Test Ingredients",
            instructions="Test Instructions",
            cooking_time=30,
            servings=4,  # Added servings field
            difficulty="Easy",
            author=self.user,
        )

        # Create some comments for the recipe
        Comment.objects.create(
            recipe=self.recipe, user=self.user, content="Test Comment 1"
        )
        Comment.objects.create(
            recipe=self.recipe, user=self.user, content="Test Comment 2"
        )

        # Create a rating for the recipe
        Rating.objects.create(recipe=self.recipe, user=self.user, value=4)

    def test_recipe_detail_view_status_code(self):
        response = self.client.get(
            reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_template(self):
        response = self.client.get(
            reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk})
        )
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")

    def test_recipe_detail_view_context(self):
        response = self.client.get(
            reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk})
        )
        self.assertEqual(response.context["recipe"], self.recipe)
        self.assertTrue("comment_form" in response.context)
        self.assertTrue("rating_form" in response.context)
        self.assertTrue("comments" in response.context)
        self.assertEqual(len(response.context["comments"]), 2)

    def test_add_comment_authenticated(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk}),
            {"form_type": "comment_form", "content": "New Test Comment"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter(recipe=self.recipe).count(), 3)

    def test_add_comment_unauthenticated(self):
        response = self.client.post(
            reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk}),
            {"form_type": "comment_form", "content": "New Test Comment"},
            follow=True,
        )
        # Should redirect to login page
        self.assertRedirects(
            response,
            "/accounts/login/?next="
            + reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk}),
        )
        # Comment count should not increase
        self.assertEqual(Comment.objects.filter(recipe=self.recipe).count(), 2)

    def test_add_rating_authenticated(self):
        # Create a new user to test adding a new rating
        new_user = User.objects.create_user(
            username="newuser", email="new@example.com", password="newpassword123"
        )
        self.client.login(username="newuser", password="newpassword123")

        response = self.client.post(
            reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk}),
            {"form_type": "rating_form", "value": "5"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.filter(recipe=self.recipe).count(), 2)
        self.assertEqual(Rating.objects.get(recipe=self.recipe, user=new_user).value, 5)

    def test_update_rating(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk}),
            {"form_type": "rating_form", "value": "3"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # Rating count should stay the same
        self.assertEqual(Rating.objects.filter(recipe=self.recipe).count(), 1)
        # Rating value should be updated
        self.assertEqual(
            Rating.objects.get(recipe=self.recipe, user=self.user).value, 3
        )


class RecipeCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.client = Client()

    def test_recipe_create_view_unauthenticated(self):
        response = self.client.get(reverse("recipes:recipe_create"))
        # Should redirect to login
        self.assertRedirects(
            response, "/accounts/login/?next=" + reverse("recipes:recipe_create")
        )

    def test_recipe_create_view_authenticated(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("recipes:recipe_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_form.html")

    def test_recipe_create_post(self):
        self.client.login(username="testuser", password="testpassword123")
        # Create a test recipe post data
        recipe_data = {
            "title": "New Test Recipe",
            "description": "New Test Description",
            "ingredients": "New Test Ingredients",
            "instructions": "New Test Instructions",
            "cooking_time": 45,
            "servings": 6,  # Added servings field
            "difficulty": "Medium",
        }

        response = self.client.post(
            reverse("recipes:recipe_create"), recipe_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recipe.objects.count(), 1)
        new_recipe = Recipe.objects.first()
        self.assertEqual(new_recipe.title, "New Test Recipe")
        self.assertEqual(new_recipe.author, self.user)


class RecipeUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpassword123"
        )
        self.client = Client()

        self.category = Category.objects.create(
            name="Test Category", description="Test Category Description"
        )

        # Create a test recipe
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            ingredients="Test Ingredients",
            instructions="Test Instructions",
            cooking_time=30,
            servings=4,  # Added servings field
            difficulty="Easy",
            author=self.user,
            category=self.category,
        )

    def test_recipe_update_view_unauthenticated(self):
        response = self.client.get(
            reverse("recipes:recipe_update", kwargs={"pk": self.recipe.pk})
        )
        # Should redirect to login
        self.assertRedirects(
            response,
            "/accounts/login/?next="
            + reverse("recipes:recipe_update", kwargs={"pk": self.recipe.pk}),
        )

    def test_recipe_update_view_not_author(self):
        self.client.login(username="otheruser", password="otherpassword123")
        response = self.client.get(
            reverse("recipes:recipe_update", kwargs={"pk": self.recipe.pk})
        )
        # Should return forbidden since user is not the author
        self.assertEqual(response.status_code, 403)

    def test_recipe_update_view_author(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(
            reverse("recipes:recipe_update", kwargs={"pk": self.recipe.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_edit.html")

    def test_recipe_update_post(self):
        self.client.login(username="testuser", password="testpassword123")
        # Update recipe data
        updated_recipe_data = {
            "title": "Updated Test Recipe",
            "description": "Updated Test Description",
            "ingredients": "Updated Test Ingredients",
            "instructions": "Updated Test Instructions",
            "cooking_time": 60,
            "servings": 8,
            "difficulty": "Hard",
            "category": self.category.id,
        }

        # Print the original recipe data for debugging
        print(f"Original title: {self.recipe.title}")

        response = self.client.post(
            reverse("recipes:recipe_update", kwargs={"pk": self.recipe.pk}),
            updated_recipe_data,
            follow=True,
        )

        # Print the response for debugging
        print(f"Response status: {response.status_code}")
        print(
            f"Response content: {response.content.decode()[:500]}..."
        )  # first 500 chars
        print(f"Response redirect chain: {response.redirect_chain}")

        # Refresh recipe from db
        self.recipe.refresh_from_db()
        print(f"Updated title: {self.recipe.title}")

        self.assertEqual(self.recipe.title, "Updated Test Recipe")
        self.assertEqual(self.recipe.cooking_time, 60)
        self.assertEqual(self.recipe.difficulty, "Hard")


class RecipeDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpassword123"
        )
        self.client = Client()

        # Create a test recipe
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            ingredients="Test Ingredients",
            instructions="Test Instructions",
            cooking_time=30,
            servings=4,  # Added servings field
            difficulty="Easy",
            author=self.user,
        )

    def test_recipe_delete_view_unauthenticated(self):
        response = self.client.get(
            reverse("recipes:recipe_delete", kwargs={"pk": self.recipe.pk})
        )
        # Should redirect to login
        self.assertRedirects(
            response,
            "/accounts/login/?next="
            + reverse("recipes:recipe_delete", kwargs={"pk": self.recipe.pk}),
        )

    def test_recipe_delete_view_not_author(self):
        self.client.login(username="otheruser", password="otherpassword123")
        response = self.client.get(
            reverse("recipes:recipe_delete", kwargs={"pk": self.recipe.pk})
        )
        # Should return forbidden since user is not the author
        self.assertEqual(response.status_code, 403)

    def test_recipe_delete_view_author(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(
            reverse("recipes:recipe_delete", kwargs={"pk": self.recipe.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_confirm_delete.html")

    def test_recipe_delete_post(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:recipe_delete", kwargs={"pk": self.recipe.pk}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Check that recipe was deleted
        self.assertEqual(Recipe.objects.count(), 0)


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpassword123"
        )
        self.client = Client()

        # Create a test recipe
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            ingredients="Test Ingredients",
            instructions="Test Instructions",
            cooking_time=30,
            servings=4,  # Added servings field
            difficulty="Easy",
            author=self.user,
        )

        # Create a test comment
        self.comment = Comment.objects.create(
            recipe=self.recipe, user=self.user, content="Test Comment"
        )

    def test_add_comment_view(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:add_comment", kwargs={"pk": self.recipe.pk}),
            {"content": "New Test Comment"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter(recipe=self.recipe).count(), 2)

    def test_edit_comment_view_get(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(
            reverse("recipes:edit_comment", kwargs={"comment_id": self.comment.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/edit_comment.html")

    def test_edit_comment_view_post(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:edit_comment", kwargs={"comment_id": self.comment.id}),
            {"content": "Updated Test Comment"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # Refresh comment from db
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Updated Test Comment")

    def test_edit_comment_view_not_author(self):
        self.client.login(username="otheruser", password="otherpassword123")
        response = self.client.get(
            reverse("recipes:edit_comment", kwargs={"comment_id": self.comment.id})
        )
        # Should return forbidden
        self.assertEqual(response.status_code, 403)

    def test_delete_comment_view_get(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(
            reverse("recipes:delete_comment", kwargs={"comment_id": self.comment.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/delete_comment_confirm.html")

    def test_delete_comment_view_post(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:delete_comment", kwargs={"comment_id": self.comment.id}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # Check that comment was deleted
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_comment_view_not_author(self):
        self.client.login(username="otheruser", password="otherpassword123")
        response = self.client.get(
            reverse("recipes:delete_comment", kwargs={"comment_id": self.comment.id})
        )
        # Should return forbidden
        self.assertEqual(response.status_code, 403)


class RatingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.client = Client()

        # Create a test recipe
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            description="Test Description",
            ingredients="Test Ingredients",
            instructions="Test Instructions",
            cooking_time=30,
            servings=4,  # Added servings field
            difficulty="Easy",
            author=self.user,
        )

    def test_add_rating_view(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:add_rating", kwargs={"pk": self.recipe.pk}),
            {"value": "4"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.filter(recipe=self.recipe).count(), 1)
        self.assertEqual(
            Rating.objects.get(recipe=self.recipe, user=self.user).value, 4
        )

    def test_update_rating_view(self):
        # Create initial rating
        Rating.objects.create(recipe=self.recipe, user=self.user, value=3)

        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:add_rating", kwargs={"pk": self.recipe.pk}),
            {"value": "5"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # Rating count should stay the same
        self.assertEqual(Rating.objects.filter(recipe=self.recipe).count(), 1)
        # Rating value should be updated
        self.assertEqual(
            Rating.objects.get(recipe=self.recipe, user=self.user).value, 5
        )

    def test_invalid_rating_value(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            reverse("recipes:add_rating", kwargs={"pk": self.recipe.pk}),
            {"value": "10"},  # Invalid value (> 5)
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        # No rating should be created
        self.assertEqual(Rating.objects.filter(recipe=self.recipe).count(), 0)


class UserRegistrationTests(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse("recipes:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/register.html")

    def test_register_view_post(self):
        user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }

        response = self.client.post(reverse("recipes:register"), user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Check if user was created
        self.assertTrue(User.objects.filter(username="newuser").exists())
        # Should redirect to login page
        self.assertRedirects(response, reverse("login"))


class JollofVarietiesTests(TestCase):
    def test_jollof_varieties_view(self):
        response = self.client.get(reverse("recipes:jollof_varieties"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_variety_detail_view_valid(self):
        valid_varieties = ["smoky", "firewood", "party", "native", "quick", "coconut"]

        for variety in valid_varieties:
            response = self.client.get(
                reverse("recipes:variety_detail", kwargs={"variety": variety})
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "recipes/variety_detail.html")
            self.assertTrue("recipe" in response.context)
            self.assertEqual(response.context["variety"], variety)

    def test_variety_detail_view_invalid(self):
        response = self.client.get(
            reverse("recipes:variety_detail", kwargs={"variety": "invalid_variety"})
        )
        # Should redirect to jollof_varieties
        self.assertRedirects(response, reverse("recipes:jollof_varieties"))


class AboutPageTests(TestCase):
    def test_about_page_view(self):
        response = self.client.get(reverse("recipes:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/about.html")
