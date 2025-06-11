from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Receipe
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Receipe)
def invalidate_receipe_cache(sender, instance, **kwargs):
    print('clearing receipe cache')
    cache.delete_pattern('*recepe_list*')