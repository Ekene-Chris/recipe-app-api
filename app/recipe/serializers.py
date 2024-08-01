"""
Serializers for recipe API
"""

from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'tags', 'time_minutes',
            'price', 'link'
        )
        read_only_fields = ['id']

class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
        model = Recipe
        fields = (
            'id', 'title', 'time_minutes',
            'price', 'link'
        )
        read_only_fields = ['id']