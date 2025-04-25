from django.db import models
from django.urls import reverse, NoReverseMatch


class TreeMenu(models.Model):
    """ Модель древовидного меню """

    name = models.CharField(max_length=75, verbose_name='Название пункта',
                            help_text='Название пункта которое будет отображено на странице')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Пункт меню для ответвлений'
    )
    menu_name = models.CharField(max_length=100, verbose_name='Название меню',
                                 help_text='Одинаковое название для всех меню одного дерева')
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

    def get_url(self):
        """ Функция получения URL """

        if self.named_url:
            try:
                if self.named_url and ',' in self.named_url:
                    named_pk = self.named_url.split(',')
                    return reverse(named_pk[0], kwargs={'pk': named_pk[1]})
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.url or '/'
        return self.url or '/'


class Page(models.Model):
    """ Модель тестовых страниц для отображения """

    name = models.CharField(max_length=75, verbose_name='Название пункта')

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.name
