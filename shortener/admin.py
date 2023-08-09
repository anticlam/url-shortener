from django.contrib import admin
from .models import Link
# Register your models here.

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display=['original_link','shortened_link']
    search_fields=['original_link','shortened_link']
    list_filter=['original_link','shortened_link']
    readonly_fields=['shortened_link']
    fieldsets=(
        ('Link',{
            'fields':(
                'original_link',
                'shortened_link',
            )
        }),
    )
