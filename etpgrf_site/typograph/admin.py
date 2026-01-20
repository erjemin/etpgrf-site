from django.contrib import admin
from .models import DailyStat

@admin.register(DailyStat)
class DailyStatAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'index_views',
        'process_requests',
        'copy_count',
        'chars_in',
        'chars_out',
        'chars_copied',
        'avg_processing_time_ms_formatted',
    )
    list_filter = ('date',)
    search_fields = ('date',)
    ordering = ('-date',)
    
    # Делаем поля только для чтения
    readonly_fields = [field.name for field in DailyStat._meta.fields]

    def has_add_permission(self, request):
        # Запрещаем добавлять записи вручную
        return False

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удалять записи
        return False

    @admin.display(description='Среднее время (мс)', ordering='total_processing_time_ms')
    def avg_processing_time_ms_formatted(self, obj):
        return f"{obj.avg_processing_time_ms:.2f}"
