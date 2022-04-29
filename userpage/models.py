import datetime

from django.db import models
from django.utils import timezone

class User(models.Model):
	user_name = models.CharField(max_length=50)
	password = models.CharField(max_length=64, default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
	start_date = models.DateTimeField('date published')
	title = models.CharField(max_length = 200)
	img = models.ImageField(upload_to = '', default = 'test.jpg')
	email = models.CharField(max_length=200)
	phone = models.CharField(default=0, max_length = 20)
	list_size = models.IntegerField(default=15)
	gender = models.CharField(max_length = 20)
	birthday = models.DateField()
	def __str__(self):
		return self.user_name
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.start_date <= now

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	op = models.CharField(max_length=50)
	pub_date = models.DateTimeField('date published')
	src = models.IntegerField(default=-1)
	share = models.BooleanField(default=0)
	post_text = models.CharField(max_length=256)
	def __str__(self):
		return self.post_text

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	pub_date = models.DateTimeField('date published')
	comment_text = models.CharField(max_length=256)
	def __str__(self):
		return self.comment_text

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.post.post_text

class Friendlink(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_send')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_get')
	accepted = models.BooleanField(default=False)
	def __int__(self):
		return self.user2