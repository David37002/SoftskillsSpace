import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("blogs/", include("blog.urls", namespace="blog")),
    path("chat/", include("chat.urls", namespace="chat")),
    path("faq/", include("faq.urls", namespace="faq")),
    path("lesson/", include("lesson.urls", namespace="lesson")),
    path("student/", include("student.urls", namespace="student")),
    path("subject/", include("subject.urls", namespace="subject")),
    path("tutor/", include("tutor.urls", namespace="tutor")),
    path("career/", include("career.urls", namespace="career")),
    path("", include("home.urls", namespace="home")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    extrapatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += extrapatterns
