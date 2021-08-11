from django.urls import include, path

from blog.api.views import (
	api_all_blog_view,
	api_blog_detail_view,
	api_blog_update_view,
	api_blog_delete_view,
	api_blog_create_view,
	ApiBlogListView
)

app_name = 'blog-api'

urlpatterns = [
	path('all/', api_all_blog_view, name="all"),
	path('<slug>/', api_blog_detail_view, name="detail"),
	path('<slug>/update', api_blog_update_view, name="update"),
	path('<slug>/delete', api_blog_delete_view, name="delete"),
	path('create', api_blog_create_view, name="create"),
	path('list', ApiBlogListView.as_view(), name='list')
]