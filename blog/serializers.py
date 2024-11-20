from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.utils import timezone


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

# class CommentSerializer(serializers.ModelSerializer):
#     # post = PostSerializer()
#     class Meta:
#         model = Comment
#         fields = ('post','parent','email','name','text')

# class PostSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True,)
#     category = CategorySerializer()
#     class Meta:
#         model= Post
#         fields = ('title','text','slug','feature_image','thumbnail_image', 'published_date','category','tags')


class PostSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)
    category = CategorySerializer()
    comments = serializers.SerializerMethodField()
    published_date = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField("get_tags")

    class Meta:
        model = Post
        fields = ('title', 'text', 'slug', 'feature_image', 'thumbnail_image', 'published_date', 'category', 'tags','comments')

    def get_published_date(self, obj):
        time_difference = timezone.now() - obj.published_date
        days = time_difference.days

        if days < 30:
            return f"{days} days ago"
        elif days < 365:
            months = days // 30
            return f"{months} month ago"
        else:
            years = days // 365
            return f"{years} year ago"
        
    def get_comments(self, obj):
        if obj:
            comment = Comment.objects.filter(post=obj).first()
            if comment:
                serializer = CommentSerializer(comment)
                return serializer.data
            else:return []
        return None
    
    def get_tags(self,obj):
        tags = obj.tags.all().values_list("name", flat=True)
        if tags:
            if len(tags) >0:
                return tags
        else:
            None

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username','phone_number','email','state','country','city','password')

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('post','email','name','text','replies')

    def get_post(self, obj):
        if obj.post:
           return obj.post.title
        return None
    
    def get_replies(self,obj):
        if obj.replies.exists():
             return CommentSerializer(obj.replies.all(),many=True).data
        else:
            return []


# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username','phone_number','email','state','country','city','password','user_profile_image')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','phone_number','email','state','country','city','password','user_profile_image')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

