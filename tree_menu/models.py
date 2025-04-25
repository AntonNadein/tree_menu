from django.db import models


class TreeMenu(models.Model):
    """ Модель древовидного меню """

    name = models.CharField(max_length=75, verbose_name='Название пункта')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Пункт меню для ответвлений'
    )
    menu_name = models.CharField(max_length=100, verbose_name='Название меню')
    url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Ссылка(URL) или именованная ссылка(named URL)'
    )
    named_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Именованная ссылка(named URL)'
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name
