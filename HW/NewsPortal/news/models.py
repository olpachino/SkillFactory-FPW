from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Описание модели Автор
class Author(models.Model):
    rating = models.FloatField(default=0.0)  # рейтинг автора

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # связь один к одному с пользователен
    
    # метод обновления рейтинга Автора
    def update_rating(self):
        posts_rating = self.posts.all().aggregate(Sum('rating'))['rating__sum']  # суммарный рейтинг все постов Автора
        comments_rating = self.user.comments.all().aggregate(Sum('rating'))['rating__sum']  # суммарный рейтинг всех комментариев Автора
        posts_comments_rating = 0  # переменная для суммарного рейтинга всех комментариев под постами автора
        for p in self.posts.all().values('id'):  # по всем постам автора
            posts_comments_rating += Comment.objects.filter(post=p['id']).aggregate(Sum('rating'))['rating__sum']  # суммируем рейтинг всех комментариев под постом
        
        self.rating = posts_rating*3 + comments_rating + posts_comments_rating  # вычисляем итоговый рейтинг
        self.save()  # фиксируем изменение
    

    def __str__(self):
        return f'{self.user.username}'


# Описание модели Категория статьи / новости
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)  # название категории имеет уникальное значение


    def __str__(self):
        return f'{self.name}'


# Описание модели Статья / Новость
class Post(models.Model):
    news = 'NW'  # сокращение для записи в БЦ
    article = 'AR'  # сокращение для записи в БД
    # отношение для вывода наименования Статья / Новость
    POSITION = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    position = models.CharField(max_length=2, choices=POSITION)  # Статья / Новость
    date = models.DateTimeField(auto_now_add=True)  # дата создания автоматически
    title = models.CharField(max_length=255)  # заголовок
    text = models.TextField()  # текст
    rating = models.FloatField(default=0.0)  # рейтинг

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')  # указатель на Автора
    category = models.ManyToManyField('Category', through='PostCategory')  # указатель на категорию

    # метод изменения рейтинга поста через like
    def like(self):
        self.rating += 1  # увеличение рейтинга осуществляется на 1 за каждый like
        self.save()

    # метод изменения рейтинга поста через dislike
    def dislike(self):
        self.rating -= 1  # уменьшение рейтинга осуществляется на 1 за каждый dislike
        self.save()

    # метот вывода первых 124 символов Статьи/Новости
    def preview(self):
        return f'{self.text[0:123]} ...'
    

    def __str__(self):
        return f'{self.title} - {self.text[:128]}'


# Описение модели для связи Категории и Статьи/Новости
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='categories')  # указатель на Статью/Новость
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')  # указатель на категорию



# Описание модели Комментарии
class Comment(models.Model):
    text = models.TextField()  # текст коментария
    date = models.DateTimeField(auto_now_add=True)  # дата комментария автоматически
    rating = models.FloatField(default=0.0)  # рейтинг

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # указатель на Новость/Статью
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # указатель на Пользователя

     # метод изменения рейтинга комментария через like
    def like(self):
        self.rating += 1  # увеличение рейтинга осуществляется на 1 за каждый like
        self.save()

    # метод изменения рейтинга комментария через dislike
    def dislike(self):
        self.rating -= 1  # уменьшение рейтинга осуществляется на 1 за каждый dislike
        self.save()

    
    def __str__(self):
        return f'{self.user.username}: {self.text[:24]}'
