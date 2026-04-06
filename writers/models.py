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


        