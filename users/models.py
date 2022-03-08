from django.db   import models

from models import TimeStampModel
from products.models import Course,CourseStat

class User(TimeStampModel):
    name                = models.CharField(max_length=50)
    phone_number        = models.CharField(max_length=50,null=True)
    profile_image       = models.URLField(max_length=300,null=True)
    description         = models.CharField(max_length=1000,null=True)
    kakao_id            = models.IntegerField(unique=True)
    is_creator          = models.BooleanField(default=False)
    email               = models.CharField(max_length=200,null=True)

    class Meta:
        db_table        = 'users'

class UserCourseStat(models.Model):
    user                = models.ForeignKey('User',on_delete=models.CASCADE)
    course_stat         = models.ForeignKey(CourseStat,on_delete=models.CASCADE)
    
    class Meta:
        db_table        = 'user_course_stats'
        constraints     = [
            models.UniqueConstraint(
                fields  =['user','course_stat'],
                name    ='unique user_course_stats',
            ),
        ]

class UserCourse(TimeStampModel):
    user                = models.ForeignKey('User',on_delete=models.CASCADE)
    course              = models.ForeignKey(Course,on_delete=models.CASCADE)

    class Meta:
        db_table        = 'user_courses'
        constraints     = [
            models.UniqueConstraint(
                fields  =['user','course'],
                name    ='unique user_courses',
            ),
        ]

class SocialAccount(models.Model):
    channel            = models.CharField(max_length=20,null=True)
    url                = models.URLField(max_length=3000,null=True)
    user               = models.ForeignKey('User',on_delete=models.CASCADE)

    class Meta:
        db_table       = 'social_accounts'