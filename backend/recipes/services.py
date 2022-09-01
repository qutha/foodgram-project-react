from django.http import HttpResponse

from recipes.models import ShoppingCart


def export_shopping_cart(request):
    user = request.user
    shopping_cart = ShoppingCart.objects.filter(user=user).all()
    ingredients_list = dict()

    for item in shopping_cart:
        for recipe_ingredient in item.recipe.recipe_ingredients.all():
            name = recipe_ingredient.ingredient.name
            measurement_unit = recipe_ingredient.ingredient.measurement_unit
            amount = recipe_ingredient.amount

            if name not in ingredients_list:
                ingredients_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            else:
                ingredients_list[name]['amount'] += amount

    filename = 'shopping-list.txt'
    content = ''

    for ingredient in ingredients_list:
        content += (
            f'{ingredient} '
            f'({ingredients_list[ingredient]["measurement_unit"]}) '
            f'— {ingredients_list[ingredient]["amount"]}\n'
        )

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename
    )
    return response
