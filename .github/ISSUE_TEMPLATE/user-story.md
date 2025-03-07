---
name: User Story:
about: Browse Recipes
title: 'User Story: Browse Recipes #1'
labels: ''
assignees: ''

---

As a user, **I want to** browse through available recipes, **so I can** discover new dishes to try and find inspiration for my cooking.

**Acceptance Criteria:**

1. Users can view a paginated list of all recipes on the database_recipes.html page
2. Recipes are displayed in reverse chronological order (newest first)
3. Each page displays up to 6 recipes
4. The home page displays 3 featured recipes (most recent ones)
5. Each recipe in the list shows basic information (title, image if available, author)

**Technical Notes:**

- Implemented using Django's ListView (RecipeListView class)
- Pagination is set to 6 items per page
- Recipe ordering is handled by the '-created_at' parameter
- The home view selects the 3 most recent recipes
