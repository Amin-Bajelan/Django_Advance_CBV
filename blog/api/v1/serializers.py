from rest_framework import serializers

from blog.models import Post, Category
from accounts.models import User,Profile


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=100)

class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snip')
    # relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolut_url = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(many=False,slug_field='name',queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'snippet', 'absolut_url', 'category', 'status', 'created_date',
                  'published_date']
        read_only_fields = ['author']

    # def get_absolut_url(self, obj):
    #     return 'test'
    def get_absolut_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get('pk'):
            rep.pop('absolut_url',None)
            rep.pop('snippet',None)
        else:
            rep.pop('context',None)
        rep['category'] = CategorySerializer(instance.category).data
        return rep
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id=self.context['request'].user.id)
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
