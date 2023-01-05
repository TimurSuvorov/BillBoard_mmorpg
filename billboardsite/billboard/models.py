import pytz as pytz
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator, MaxLengthValidator
from django.db import models


TIMEZONES = list(zip(pytz.all_timezones, pytz.all_timezones))

class Announcement(models.Model):
    title = models.CharField(max_length=254,
                             unique=True,
                             db_index=True,
                             verbose_name='Заголовок')
    content = models.TextField(validators=[MinLengthValidator(4)],
                               verbose_name='Содержание')
    #media_content
    is_published = models.BooleanField(default=True,
                                       verbose_name='Публикация')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата редактирования')
    category = models.ForeignKey(to='Category',
                                 on_delete=models.CASCADE,
                                 related_name='cat_announcements',
                                 verbose_name='Категория')
    author_ann = models.ForeignKey(to=User,
                                   on_delete=models.SET('Lost(deleted) Stranger'),
                                   related_name='auth_announcements',
                                   verbose_name='Автор объявлений')

    num_replies = models.IntegerField(default=0, verbose_name='Количество откликов')

    def __str__(self):
        return f'{self.title}'

    @property
    def count_replies(self):
        replies_num = self.reply_set.all().count()
        self.num_replies = replies_num
        return replies_num

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'


class Category(models.Model):
    catname = models.CharField(max_length=64,
                               unique=True,
                               verbose_name='Категория')

    slug = models.SlugField(max_length=64,
                            unique=True,
                            db_index=True,
                            verbose_name='URL',
                            null=True)

    def __str__(self):
        return f'{self.catname}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Reply(models.Model):
    announcement = models.ForeignKey(to=Announcement,
                                     related_name='relies',
                                     on_delete=models.CASCADE)
    content =models.TextField(validators=[MinLengthValidator(4)],
                              verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата редактирования')
    author_repl = models.ForeignKey(to=User,
                                    on_delete=models.SET('Lost(deleted) Stranger'),
                                    related_name='auth_replies',
                                    verbose_name='Автор отликов')


    def __str__(self):
        return f'{self.catname}'

    class Meta:
        verbose_name = 'Отлик'
        verbose_name_plural = 'Отлики'


class Newsletter(models.Model):
    title = models.CharField(max_length=254,
                             unique=True,
                             db_index=True,
                             verbose_name='Заголовок')
    text_content = models.TextField(validators=[MinLengthValidator(4)],
                                    verbose_name='Содержание(текст)')
    # media_content
    category = models.ForeignKey(to='Category',
                                 on_delete=models.CASCADE,
                                 related_name='cat_newsletters',
                                 verbose_name='Категория')
    is_ready = models.BooleanField(default=True,
                                   verbose_name='Готовность')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class UserProfile(models.Model):
    nickname = models.CharField(max_length=64,
                                blank=False,
                                validators=[RegexValidator(r'^[a-zA-Z]+[0-9a-zA-Z]*$',
                                                          'Никнейм должен быть буквенно-цифровым и начинаться с букву')],
                                help_text='Никнейм должен быть буквенно-цифровым и начинаться с букву',
                                verbose_name='Никнейм'
                                )
    aboutme = models.CharField(max_length=1024)
    timezone = models.CharField(max_length=64,
                                choices=TIMEZONES,
                                default='UTC',
                                verbose_name='Timezone')
    is_declains_display = models.BooleanField(default=True,
                                              verbose_name='Показать удаленные отлики')
    is_replies_alerts = models.BooleanField(default=True,
                                            verbose_name='Оповещение новых отликов')
    is_news_subscribe = models.BooleanField(default=True,
                                            verbose_name='Подписка на рассылку')