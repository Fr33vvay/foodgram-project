from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, Subscribe, User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    def validate(self, data):
        """Запрещает подписаться второй раз"""
        super().validate(data)
        user = self.context.get('request_user')
        author = self.context.get('author')
        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError('Подписка уже существует')
        return data

    def validate_id(self, data):
        """Запрещает подписаться на самого себя"""
        super().validate(data)
        user = self.context.get('request_user')
        if user == data:
            raise ValidationError('Вы не можете подписаться на себя')
        return data

    class Meta:
        fields = ('user', 'author')
        model = Subscribe
