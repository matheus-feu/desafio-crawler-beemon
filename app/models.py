from django.db import models


class MoviesModels(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    duration = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    votes = models.CharField(max_length=100)
    img_url = models.URLField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
