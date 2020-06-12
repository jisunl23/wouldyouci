from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime
from movies.models import Movie, Premovie
from cinemas.models import Cinema
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


def profile_path(instance, filename):
    filename = datetime.today().strftime('%Y%m%d%H%M%f')
    return f'profile/{filename}.jpeg'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, get_agreement, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            email=email,
            get_agreement=get_agreement,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, get_agreement, email, password=None):
        user = self.create_user(
            username,
            email=email,
            password=password,
            get_agreement=get_agreement,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    get_agreement = models.BooleanField(default=False)
    pick_movies = models.ManyToManyField(Movie, related_name='pick_users')
    pick_cinemas = models.ManyToManyField(Cinema, related_name='pick_users')
    pick_premovies = models.ManyToManyField(Premovie, related_name='pick_users')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'get_agreement']

    def __str__(self):
        return '%s' % self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name='file', on_delete=models.CASCADE)
    file = ProcessedImageField(
        processors=[ResizeToFill(200, 200)],
        upload_to=profile_path,
        format='JPEG',
        options={'quality': 80},
    )

    def __str__(self):
        return 'media/%s' % self.file


class Rating(models.Model):
    comment = models.TextField(blank=True, null=True)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        ordering = ('-updated_at',)


class CinemaRating(models.Model):
    comment = models.TextField(blank=True, null=True)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='cinema_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cinema_ratings')

    class Meta:
        ordering = ('-updated_at',)
