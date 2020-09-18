from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Subject(models.Model):
    subject_name=models.CharField(max_length=75,default='Extras')
    description=models.CharField(max_length=2000,default='')

    def __str__(self):
        return 'Subject name: ' + self.subject_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    points_scored = models.IntegerField(default=0)
    questions_attempted = models.CharField(max_length=2000, default='')
    bio = models.TextField()

    def __str__(self):
        return self.user.username + ' Points Scored: ' + \
               str(self.points_scored) + ' Questions Attempted: ' + \
               self.questions_attempted

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()




# class User(User):
#     name = models.CharField(max_length=75)





class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=300)
    timeout = models.IntegerField(default=75)
    points = models.IntegerField(default=1)

    def __str__(self):
        """
        Function for representing the question in correct format
        :return: str object
        """
        return 'Question: ' + self.question_text + \
               ' \nTimeout (seconds):' + str(self.timeout) + \
               ' \nPoints :' + str(self.points)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=200)

    def __str__(self):
        """
        Function for representing the question in correct format
        :return: str object
        """
        return 'Option 1: ' + self.option1 + ' \nOption 2: ' + \
               self.option2 +  ' \nOption 3: ' + self.option3 + \
               ' \nOption 4: ' + self.option4 + \
               ' \nAnswer: ' + self.correct_option
