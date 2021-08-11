from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication

from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def api_all_blog_view(request):
	blogs = BlogPost.objects.all()
	if request.method == 'GET':
		if blogs:
			serializer = BlogPostSerializer(blogs, many=True)
			return Response(serializer.data)
		return Response(status.HTTP_404_NOT_FOUND)



@api_view(['GET',])
@permission_classes([IsAuthenticated]) # The user must be authenticated to see the post
def api_blog_detail_view(request, slug):
	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = BlogPostSerializer(blog_post)
		return Response(serializer.data)


@api_view(['PUT',])
@permission_classes([IsAuthenticated]) # The user must be authenticated as well as the same user who created the post in order to update its content
def api_blog_update_view(request, slug):
	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response': 'You are not the one who created this post, So you are not allowed to edit it'})

	if request.method == 'PUT':
		serializer = BlogPostSerializer(blog_post, data=request.data)
		data = {}

		if serializer.is_valid():
			serializer.save()
			data['success'] = True
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE',])
@permission_classes([IsAuthenticated]) # The user must be authenticated as well as the same user who created the post in order to delete the post
def api_blog_delete_view(request, slug):
	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response': 'You are not the one who created this post, So you are not allowed to delete it'})

	if request.method == 'DELETE':
		operation = blog_post.delete()
		data = {}
		data['success'] = True if operation else False
		return Response(data=data)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def api_blog_create_view(request):
	account = request.user
	blog_post = BlogPost(author=account)

	if request.method == 'POST':
		serializer = BlogPostSerializer(blog_post, data=request.data)
		if serializer.is_valid():
			try:
				serializer.save()
			except:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ApiBlogListView(ListAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination