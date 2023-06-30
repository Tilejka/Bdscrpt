from django.db import models

from users.models import User


class WorldType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'world type'
        verbose_name_plural = 'worlds types'

    def __str__(self):
        return self.name


class DivineRank(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'divine_rank'
        verbose_name_plural = 'divine_ranks'

    def __str__(self):
        return self.name


class Alignment(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'alignment'
        verbose_name_plural = 'alignments'

    def __str__(self):
        return self.name


class Domain(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'domain'
        verbose_name_plural = 'domains'

    def __str__(self):
        return self.name


class WorldGod(models.Model):
    name = models.CharField(max_length=128)
    alignment = models.ForeignKey(to=Alignment, on_delete=models.CASCADE)
    domains = models.ForeignKey(to=Domain, on_delete=models.CASCADE)
    rank = models.ForeignKey(to=DivineRank, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='deities_images')

    class Meta:
        verbose_name = 'world god'
        verbose_name_plural = 'worlds gods'

    def __str__(self):
        return self.name


class World(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='world_images')
    world_type = models.ForeignKey(to=WorldType, on_delete=models.CASCADE)
    world_gods = models.ForeignKey(to=WorldGod, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    fav_world = models.ManyToManyField(to=User, related_name='fav_world', blank=True)

    class Meta:
        verbose_name = 'world'
        verbose_name_plural = 'worlds'

    def __str__(self):
        return self.name


class WComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey('World', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username
