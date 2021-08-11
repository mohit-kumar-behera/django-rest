from rest_framework import serializers

from blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    # To link the user to the blog post
    username = serializers.SerializerMethodField('get_username_from_author')
    
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'date_published', 'username']

    def get_username_from_author(self, blog_post):
        username = blog_post.author.username
        return username



