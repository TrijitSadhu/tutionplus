"""
Signals for bank app - Auto-update info tables for mcq and current_affairs
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from bank.models import mcq, mcq_info_2018, mcq_info_2019, mcq_info_2020, mcq_info_2025, mcq_info_2026, mcq_info_2027, mcq_info_2028, current_affairs, current_affairs_info_2018, current_affairs_info_2019, current_affairs_info_2020, current_affairs_info_2025, current_affairs_info_2026, current_affairs_info_2027, current_affairs_info_2028


@receiver(post_save, sender=mcq)
def update_mcq_info_on_save(sender, instance, created, **kwargs):
    """
    Auto-update mcq_info tables when MCQ is saved.
    Recalculates pagination and month lists for the year.
    """
    try:
        if instance.year_now == '2018':
            info = mcq_info_2018.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2019':
            info = mcq_info_2019.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2020':
            info = mcq_info_2020.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2025':
            info = mcq_info_2025.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2026':
            info = mcq_info_2026.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2027':
            info = mcq_info_2027.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2028':
            info = mcq_info_2028.objects.all().first()
            if info:
                info.save()
    except Exception as e:
        print(f"Error updating mcq_info: {e}")


@receiver(post_save, sender=current_affairs)
def update_current_affairs_info_on_save(sender, instance, created, **kwargs):
    """
    Auto-update current_affairs_info tables when Current Affairs is saved.
    Recalculates pagination and month lists for the year.
    """
    try:
        if instance.year_now == '2018':
            info = current_affairs_info_2018.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2019':
            info = current_affairs_info_2019.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2020':
            info = current_affairs_info_2020.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2025':
            info = current_affairs_info_2025.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2026':
            info = current_affairs_info_2026.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2027':
            info = current_affairs_info_2027.objects.all().first()
            if info:
                info.save()
        elif instance.year_now == '2028':
            info = current_affairs_info_2028.objects.all().first()
            if info:
                info.save()
    except Exception as e:
        print(f"Error updating current_affairs_info: {e}")
