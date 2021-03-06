import random
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from universities.utils import unique_slug_generator
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "programmes/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

class ProgrammeQuerySet(models.query.QuerySet):
    # def active(self):
    #     return self.filter(active=True)
    #
    # def featured(self):
    #     return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                  Q(description__icontains=query) |
                  Q(fee__icontains=query)
                  )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()


class ProgrammeManager(models.Manager):
    def get_queryset(self):
        return ProgrammeQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    # def featured(self): #Product.objects.featured()
    #     return self.get_queryset().featured()

    def get_by_id(self, pk):
        qs = self.get_queryset().filter(id=pk) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().all().search(query)


class Programme(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True,unique=True)
    description = models.TextField()
    image       = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    fee         = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)


    objects = ProgrammeManager()


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/programmes/{slug}".format(slug=self.slug)

    @property
    def name(self):
        return self.title

def programme_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(programme_pre_save_receiver,sender = Programme)
