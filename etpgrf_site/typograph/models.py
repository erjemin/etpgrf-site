from django.db import models
from django.utils import timezone

class DailyStat(models.Model):
    """
    Модель для хранения агрегированной статистики использования за день.
    """
    date = models.DateField(
        verbose_name="Дата",
        unique=True,
        default=timezone.now
    )
    
    # Основные метрики
    index_views = models.PositiveIntegerField(
        verbose_name="Просмотры главной",
        default=0
    )
    process_requests = models.PositiveIntegerField(
        verbose_name="Запросы на обработку",
        default=0
    )
    copy_count = models.PositiveIntegerField(
        verbose_name="Копирований в буфер",
        default=0
    )
    
    # Объемы
    chars_in = models.BigIntegerField(
        verbose_name="Символов на входе",
        default=0
    )
    chars_out = models.BigIntegerField(
        verbose_name="Символов на выходе",
        default=0
    )
    chars_copied = models.BigIntegerField(
        verbose_name="Символов скопировано",
        default=0
    )
    
    # Производительность
    total_processing_time_ms = models.FloatField(
        verbose_name="Суммарное время обработки (мс)",
        default=0.0
    )
    
    # Статистика по использованным настройкам
    settings_stats = models.JSONField(
        verbose_name="Статистика настроек",
        default=dict
    )

    class Meta:
        verbose_name = "Дневная статистика"
        verbose_name_plural = "Дневная статистика"
        ordering = ['-date']

    def __str__(self):
        return f"Статистика за {self.date.strftime('%Y-%m-%d')}"

    @property
    def avg_processing_time_ms(self):
        """Среднее время обработки одного запроса."""
        if self.process_requests == 0:
            return 0.0
        return self.total_processing_time_ms / self.process_requests
