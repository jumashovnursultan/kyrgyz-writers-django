from django.db import models
from django.contrib.auth.models import User


class Writer(models.Model):
    LANGUAGE_CHOICES = [
        ('kyrgyz', 'Кыргызча'),
        ('russian', 'Орусча'),
        ('both', 'Эки тилде'),
    ]

    name = models.CharField(max_length=200, verbose_name="Имя писателя")
    birth_year = models.IntegerField(verbose_name="Год рождения")
    death_year = models.IntegerField(null=True, blank=True, verbose_name="Год смерти")
    biography = models.TextField(verbose_name="Биография")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name="Фото")
    epoch = models.CharField(max_length=100, verbose_name="Эпоха/Период")
    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='kyrgyz',
        verbose_name="Язык творчества"
    )
    tags = models.CharField(
        max_length=300, blank=True,
        verbose_name="Теги (через запятую)",
        help_text="Например: патриотизм, природа, любовь"
    )

    def __str__(self):
        return self.name

    def get_language_display_ky(self):
        mapping = {'kyrgyz': 'Кыргызча', 'russian': 'Орусча', 'both': 'Эки тилде'}
        return mapping.get(self.language, self.language)

    class Meta:
        verbose_name = "Писатель"
        verbose_name_plural = "Писатели"


class Quote(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name='quotes', verbose_name="Жазуучу")
    text = models.TextField(verbose_name="Цитата")

    def __str__(self):
        return f"{self.writer.name}: {self.text[:50]}"

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаталар"


class Work(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name='work_set')
    title = models.CharField(max_length=200, verbose_name="Название")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год")
    genre = models.CharField(max_length=100, blank=True, verbose_name="Жанр")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'writer')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.user.username} -> {self.writer.name}"
