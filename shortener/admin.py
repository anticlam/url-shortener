from django.contrib import admin
from .models import Link
# Register your models here.

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display=['original_link','shortened_link', 'created_at', 'id']
    search_fields=['original_link','shortened_link', 'created_at', 'id']
    list_filter=['original_link','shortened_link', 'created_at', 'id']
    readonly_fields=['shortened_link']
    fieldsets=(
        ('Link',{
            'fields':(
                'original_link',
                'shortened_link',
                'created_at',
                'id',
            )
        }),
    )
