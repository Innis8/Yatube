import shutil
import tempfile
from datetime import datetime
from django.urls import reverse
from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Group, Post, Follow

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)

        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.group_without_needed_post = Group.objects.create(
            title='Группа без нужного поста',
            slug='group-without-needed-post',
            description='Описание группы без нужного поста',
        )

        cls.post = Post.objects.create(
            author=cls.author,
            pub_date=datetime.now(),
            text='Тестовый пост для проверки',
            group=cls.group,
            image=cls.uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_namespace_uses_correct_template(self):
        """namespace:name использует соответствующий шаблон"""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_posts',
                kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.author}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_post(self, first_object):
        self.assertEqual(first_object.author, self.author)
        self.assertEqual(first_object.text, 'Тестовый пост для проверки')
        self.assertEqual(first_object.group, self.group)
        self.assertEqual(first_object.image, 'posts/small.gif')

    def test_index_page_show_correct_context(self):
        """
        Содержимое поста на главной странице должно соответствовать ожиданиям
        """
        response = self.authorized_author.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)

    def test_group_page_show_correct_context(self):
        """
        Содержимое поста на странице группы должно соответствовать ожиданиям.
        """
        response = self.authorized_author.get(reverse(
            'posts:group_posts',
            kwargs={'slug': 'test-slug'}
        )
        )
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)

    def test_profile_page_show_correct_context(self):
        """
        Содержимое поста на странице профиля должно соответствовать ожиданиям.
        """
        response = self.authorized_author.get(reverse(
            'posts:profile',
            kwargs={'username': self.author}
        )
        )
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)

    def test_post_detail_page_show_correct_context(self):
        """
        Содержимое страницы поста должно соответствовать ожиданиям.
        """
        response = self.authorized_author.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        )
        )
        first_object = response.context['post']
        self.check_post(first_object)

    def test_edit_page_show_correct_context(self):
        """
        Содержимое страницы редактирования поста должно соответствовать
        ожиданиям.
        """
        response = self.authorized_author.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': self.post.id}
        )
        )
        first_object = response.context['post']
        self.check_post(first_object)
        print(response.context['post'])

    def test_post_appears_on_index_page(self):
        """
        Тест того, что пост с данным содержанием и с принадлежностью к данной
        группе был успешно создан.
        """
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост для проверки',
                group=self.group
            ).exists()
        )

    def test_post_not_in_another_group(self):
        """
        Пост не попал в группу, для которой не был предназначен, то есть,
        он там отсутствует.
        """
        self.assertFalse(
            Post.objects.filter(
                text='Тестовый пост для проверки',
                group=self.group_without_needed_post
            ).exists()
        )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CommentViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)
        cls.user = User.objects.create_user(username='user')
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)
        cls.guest_client = Client()

        cls.post = Post.objects.create(
            author=cls.author,
            pub_date=datetime.now(),
            text='Тестовый пост',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_comment_authorized_user_can(self):
        """
        Авторизованный юзер может комментить
        """
        self.authorized_user.post(reverse(
            'posts:add_comment',
            kwargs={'post_id': self.post.id}
        ),
            {'text': 'Тестовый комментарий', },
            follow=True
        )
        response = self.authorized_user.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        ),
        )
        self.assertContains(response, 'Тестовый комментарий')

    def test_comment_unauthorized_user_cant(self):
        """
        Неавторизованный юзер комментить не может
        """
        self.guest_client.post(reverse(
            'posts:add_comment',
            kwargs={'post_id': self.post.id}
        ),
            {'text': '2 Тестовый комментарий 2', },
            follow=True
        )
        response = self.guest_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        ),
        )
        self.assertNotContains(response, '2 Тестовый комментарий 2')


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)
        cls.user = User.objects.create_user(username='follower')
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)

        cls.post = Post.objects.create(
            author=cls.author,
            pub_date=datetime.now(),
            text='1 Тестовый пост 1',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_authorized_user_can_follow(self):
        """
        Авторизованный пользователь может подписываться на других пользователей
        """
        self.authorized_user.get(
            reverse('posts:profile_follow', kwargs={'username': self.author})
        )
        self.assertTrue(Follow.objects.filter(
            author=self.author,
            user=self.user).exists()
        )

    def test_followed_author_posts_shows_in_followers_feed(self):
        """
        Новая запись пользователя появляется в ленте тех, кто на него подписан
        не появляется в ленте тех, кто не подписан.
        """
        self.authorized_user.get(
            reverse('posts:profile_follow', kwargs={'username': self.author})
        )
        response = self.authorized_user.get(reverse('posts:follow_index'))
        followed_post = response.context['page_obj'].object_list[0]
        self.assertEqual(followed_post, self.post)
        response = self.authorized_author.get(reverse('posts:follow_index'))
        self.assertEqual(response.context['paginator'].count, 0)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UnFollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)
        cls.user = User.objects.create_user(username='follower')
        cls.authorized_user = Client()
        cls.authorized_user.force_login(cls.user)

        cls.post = Post.objects.create(
            author=cls.author,
            pub_date=datetime.now(),
            text='1 Тестовый пост 1',
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_authorized_user_can_unfollow(self):
        """
        Авторизованный пользователь может удалять других пользователей
        из подписок
        """
        self.authorized_user.get(reverse(
            'posts:profile_unfollow', kwargs={'username': self.author})
        )
        self.assertFalse(Follow.objects.filter(
            author=self.author,
            user=self.user).exists()
        )
