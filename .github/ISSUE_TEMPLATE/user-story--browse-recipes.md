---
name: 'User Story: Browse Recipes'
about: Browse Recipes
title: ''
labels: ''
assignees: ''

---

As a logged-in user, **I want to** assess different varieties of Nigeria Jollof recipes, **So that** I can learn how to prepare different varieties of Nigerian jollof rice.

**Acceptance Criteria:**
- [ ] Users can view a paginated list of all recipes on the database_recipes.html page
- [ ] Recipes are displayed in reverse chronological order (newest first)
- [ ] Each page displays up to 6 recipes
- [ ] The home page displays 3 featured recipes (most recent ones)
- [ ] Each recipe in the list shows basic information (title, image if available, author)

**Technical Notes:**
- [ ] Implemented using Django's ListView (RecipeListView class) 
- [ ] Pagination is set to 6 items per page 
- [ ] Recipe ordering is handled by the '-created_at' parameter 
- [ ] The home view selects the 3 most recent recipes
