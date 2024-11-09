from django.db import models

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    """
    Класс Статьи (Поста)
    """

    title = models.CharField(max_length=150, verbose_name="заголовок")
    slug = models.CharField(max_length=150, verbose_name="slug", **NULLABLE)
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to="blog/preview", verbose_name="изображение", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')
    view_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = (
            "-created_at",
        )

    def __str__(self):
        return f"{self.title}"
