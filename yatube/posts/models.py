from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Группа',
        help_text='Название группы'
    )
    slug = models.SlugField(
        max_length=50, unique=True,
        verbose_name='Читабельная slug-ссылка',
        help_text='Может состоять из символов латиницы, '
        'цифр, нижнего подчеркивания и дефиса '
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Расскажите, о чём эта группа'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Текст нового или редактируемого поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
        help_text='Время создание поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой относится пост. Необязательно.'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Картинка необязательна',
        upload_to='posts/',
        blank=True
    )
    tag = models.ManyToManyField(Tag, through='TagPost')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост комментария',
        help_text='Пост, к которому относится комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
        help_text='Автор комментария'
    )
    text = models.TextField(
        max_length=1000,
        verbose_name='Текст комментария',
        help_text='Написать комментарий'
    )
    created = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подпишитесь на избранного автора'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Избранный автор',
        help_text='На избранного автора подписываются'
    )

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Избранный автор'
        verbose_name_plural = 'Избранные авторы'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follower'
            ),
        )

    def __str__(self):
        return f'{self.user.username}-->@{self.author.username}'


class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.post}'
