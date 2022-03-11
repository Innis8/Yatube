from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Group, Post, Comment, Follow

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост длиной больше 15 символов',
        )

    def test_post_models_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_value = post.text[:15]
        self.assertEqual(expected_value, str(post))

    def test_verbose_name_post_model(self):
        """Проверяем, что verbose_name в полях - ожидаемый"""
        post = PostModelTest.post
        verbose_field = {
            'text': 'Текст поста',
            'pub_date': 'Время создания',
            'author': 'Автор',
            'group': 'Группа',
            'image': 'Картинка'
        }
        for value, expected_value in verbose_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name,
                    expected_value
                )

    def test_help_text_post_model(self):
        """Проверяем, что help_text в полях - ожидаемый"""
        post = PostModelTest.post
        help_field = {
            'text': 'Текст нового или редактируемого поста',
            'pub_date': 'Время создание поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой относится пост. Необязательно.'
        }
        for value, expected_value in help_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text,
                    expected_value
                )


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    def test_group_models_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = GroupModelTest.group
        expected_value = group.title
        self.assertEqual(expected_value, str(group))

    def test_verbose_name_group_model(self):
        """Проверяем, что verbose_name в полях - ожидаемый"""
        group = GroupModelTest.group
        verbose_field = {
            'title': 'Группа',
            'slug': 'Читабельная slug-ссылка',
            'description': 'Описание группы',
        }
        for value, expected_value in verbose_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name,
                    expected_value
                )

    def test_help_text_group_model(self):
        """Проверяем, что help_text в полях - ожидаемый"""
        group = GroupModelTest.group
        help_field = {
            'title': 'Название группы',
            'slug': (
                'Может состоять из символов латиницы, '
                'цифр, нижнего подчеркивания и дефиса '
            ),
            'description': 'Расскажите, о чём эта группа',
        }
        for value, expected_value in help_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text,
                    expected_value
                )


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост длиной больше 15 символов',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментарий',
        )

    def test_comment_models_have_correct_object_names(self):
        """Проверяем, что у модели Comment корректно работает __str__."""
        comment = CommentModelTest.comment
        expected_value = comment.text
        self.assertEqual(expected_value, str(comment))

    def test_verbose_name_comment_model(self):
        """Проверяем, что verbose_name в полях - ожидаемый"""
        comment = CommentModelTest.comment
        verbose_field = {
            'post': 'Пост комментария',
            'author': 'Автор',
            'text': 'Текст комментария',
        }
        for value, expected_value in verbose_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).verbose_name,
                    expected_value
                )

    def test_help_text_comment_model(self):
        """Проверяем, что help_text в полях - ожидаемый"""
        comment = CommentModelTest.comment
        help_field = {
            'post': 'Пост, к которому относится комментарий',
            'author': 'Автор комментария',
            'text': 'Написать комментарий',
        }
        for value, expected_value in help_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).help_text,
                    expected_value
                )


class FollowtModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.user = User.objects.create_user(username='follower')
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author
        )

    def test_follow_models_have_correct_object_names(self):
        """Проверяем, что у модели Comment корректно работает __str__."""
        follow = FollowtModelTest.follow
        expected_value = (f'{self.user.username}-->@{self.author.username}')
        self.assertEqual(expected_value, str(follow))

    def test_verbose_name_follow_model(self):
        """Проверяем, что verbose_name в полях - ожидаемый"""
        follow = FollowtModelTest.follow
        verbose_field = {
            'user': 'Подписчик',
            'author': 'Избранный автор',
        }
        for value, expected_value in verbose_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    follow._meta.get_field(value).verbose_name,
                    expected_value
                )

    def test_help_text_follow_model(self):
        """Проверяем, что help_text в полях - ожидаемый"""
        follow = FollowtModelTest.follow
        help_field = {
            'user': 'Подпишитесь на избранного автора',
            'author': 'На избранного автора подписываются',
        }
        for value, expected_value in help_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    follow._meta.get_field(value).help_text,
                    expected_value
                )
