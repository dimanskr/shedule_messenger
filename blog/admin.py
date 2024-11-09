from django.contrib import admin
from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "preview",
        "created_at",
        "is_published",
        "view_count",
    )
    list_editable = (
        "preview",
        "is_published",
    )
    list_filter = ("is_published",)
    search_fields = (
        "title",
        "body",
    )
    list_display_links = ("title",)
    ordering = ('-created_at',)
