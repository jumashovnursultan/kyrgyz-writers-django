from django.db import models

class Writer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя писателя")
    birth_year = models.IntegerField(verbose_name="Год рождения")
    death_year = models.IntegerField(null=True, blank=True, verbose_name="Год смерти")
    biography = models.TextField(verbose_name="Биография")
    works = models.TextField(verbose_name="Известные произведения")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name="Фото")
    epoch = models.CharField(max_length=100, verbose_name="Эпоха/Период")

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

        