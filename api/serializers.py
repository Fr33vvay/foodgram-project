from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, Subscribe, User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault())
    author = serializers.SlugRelatedField(queryset=User.objects.all(),
                                          slug_field='id')

    def validate(self, data):
        user = self.context['request'].user
        if user == data['author']:
            raise serializers.ValidationError('Нельзя подписаться '
                                              'на себя самого')
        return data

    class Meta:
        fields = ('user', 'author')
        model = Subscribe
        validators = [
            UniqueTogetherValidator(queryset=Subscribe.objects.all(),
                                    fields=('user', 'author'))
        ]
