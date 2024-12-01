from datetime import datetime

from app.models.category import Category
from app.models.ingredient import Ingredient
from app.models.recipe_ingredients import RecipeIngredient
from app.models.user import User
from app.models.user_progress import UserProgress
from app.models.review import Review
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.step import Step
from app.models.instruction_step import InstructionStep

from app.database.database import get_session_with

with get_session_with() as session:

    ## ADD EXAMPLE OBJECT TO DB

    # Add Category
    new_category = Category(name = "Picie", description = "do picia z kolegami")

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    # ADD User
    new_user = User(
    username="john_doe",
    email="john.doe@example.com",
    password="test",  # W praktyce hasło powinno być haszowane
    date_of_birth=datetime(1990, 1, 1),
    creation_date=datetime.now()
    )

    # Add Recipe
    new_recipe = Recipe(
    name="Mojito",
    image_url="/images/mojito.jpg",
    preparation_time=0,
    creation_time=datetime.now(),
    last_modified=datetime.now(),
    description = "bardzo smaczny drink",
    alcohol_content = 0.02,
    average_rating = 0,
    number_of_reviews = 0,
    difficulty = 2
    )

    new_recipe.category = new_category
    new_recipe.user = new_user

    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)


    # ADD Review

    new_review = Review(
    comment="Świetny przepis! Smakowało całej rodzinie.",
    rating=5,
    creation_date=datetime.now(),  # ustawia bieżącą datę i godzinę
    recipe_id = new_recipe.recipe_id,
    user_id = new_user.user_id,
    )

    session.add(new_review)
    session.commit()
    session.refresh(new_review)


    # ADD Ingridient

    new_ingredient = Ingredient(
    name = 'jajka',
    type = 'nabial'
    )

    session.add(new_ingredient)
    session.commit()
    session.refresh(new_ingredient)


    # ADD RecipeIngridient

    new_recipe_ingredient = RecipeIngredient(
    quantity = 3,
    unit = 'kg',
    ingredient = new_ingredient,
    recipe = new_recipe
    )

    session.add(new_recipe_ingredient)
    session.commit()
    session.refresh(new_recipe_ingredient)

    # ADD Step

    new_step = Step(
    name = 'Add water',
    description = 'Add 200 ml of water',
    step_number = 1,
    duration = 100
    )

    session.add(new_step)
    session.commit()
    session.refresh(new_step)


    # ADD RecipeStep

    new_recipe_step = InstructionStep(
    recipe = new_recipe,
    step = new_step
    )

    session.add(new_recipe_step)
    session.commit()
    session.refresh(new_recipe_step)


    # ADD User_Progress
    new_user_progress = UserProgress(
    started_date = datetime.now(),
    finished_date = datetime.now(),
    completed = False,
    user_id = new_user.user_id,
    recipe_id = new_recipe.recipe_id,
    instruction_steps_id = new_recipe_step.ingredient_step_id
    )

    session.add(new_user_progress)
    session.commit()
    session.refresh(new_user_progress)

    # LIST ALL Recipe

    result = session.query(Recipe).all()

    for recipe in result:
        print(f"ID: {recipe.recipe_id}, Name: {recipe.name}")
