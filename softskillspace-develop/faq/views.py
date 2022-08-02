from django.db.models import Q
from django.views.generic import ListView

from faq.models import FAQ, FaqCategory
from softskillspace.utils.query import get_query


class IndexView(ListView):
    template_name = "faq/index.html"
    context_object_name = "faqs"
    paginate_by = 25
    model = FAQ

    def get_queryset(self):
        keyword = self.request.GET.get("keyword")
        query = Q(visible=True)

        if keyword:
            query &= get_query(keyword, "name", "content")

        faqs = FAQ.items.filter(query)
        return faqs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = FaqCategory.items.order_by("name")

        extra_context = {"tags": tags}

        context.update(extra_context)
        return context
