from django.db.models import Count
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from blog.models import Blog, Category

# Create your views here.


class BlogListView(ListView):
    model = Blog
    paginate_by = 21
    context_object_name = "blogs"
    template_name = "blog/list.html"

    def get_queryset(self):
        return Blog.items.all().select_related("category")


class BlogDetailView(DetailView):
    model = Blog
    lookup_field = "slug"
    context_object_name = "blog"
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()

        related_articles = (
            Blog.objects.filter(category=blog.category_id)
            .exclude(id=blog.id)
            .select_related("category")
        )

        tags = Category.items.annotate(
            blog_count=Count("blog")).order_by("-blog_count")

        context["tags"] = tags[:20]
        context["related_articles"] = related_articles
        return context
