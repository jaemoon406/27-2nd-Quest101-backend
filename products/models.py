from django.db   import models

from models import TimeStampModel
        
class Course(TimeStampModel):
    name                 = models.CharField(max_length=45, null=True)
    thumbnail_image_url  = models.URLField(max_length=3000, null=True)
    description          = models.TextField(max_length=1000,null=True)
    price                = models.DecimalField(max_digits=10, null=True, decimal_places=2)
    start_date           = models.DateTimeField(null=True)
    end_date             = models.DateTimeField(null=True)
    limit                = models.IntegerField(null=True)
    payment_period       = models.IntegerField(null=True)
    user                 = models.ForeignKey('users.User',on_delete=models.CASCADE)
    sub_category         = models.ForeignKey('SubCategory',null = True, on_delete=models.CASCADE)
    level                = models.ForeignKey('Level', null=True, on_delete=models.CASCADE)
    course_status        = models.ForeignKey('CourseStatus', on_delete=models.CASCADE)
    discount_rate        = models.IntegerField(default=0, null=True)
    
    class Meta:
        db_table        = 'courses'

class Media(models.Model):
    url                 = models.URLField(max_length=3000)
    type                = models.CharField(max_length=20)
    course              = models.ForeignKey('Course',on_delete=models.CASCADE)

    class Meta:
        db_table        = 'medias'

class Level(models.Model):
    level               = models.CharField(max_length=45)
    
    class Meta:
        db_table        = 'levels'  

class CourseStatus(models.Model):
    status = models.CharField(max_length=30)
    
    class Meta:
        db_table        = 'coursestatus'

class Comment(TimeStampModel):
    content             = models.CharField(max_length=400)
    user                = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course              = models.ForeignKey('Course', on_delete=models.CASCADE)
    
    class Meta:
        db_table        = 'comments'

class Stat(models.Model):
    name                = models.CharField(max_length=10,unique=True)

    class Meta:
        db_table        = 'stats'

class CourseStat(models.Model):
    course              = models.ForeignKey('Course',on_delete=models.CASCADE)
    stat                = models.ForeignKey('Stat',on_delete=models.CASCADE)
    score               = models.IntegerField(default=0)

    class Meta:
        db_table        = 'course_stats'
        constraints     = [
            models.UniqueConstraint(
                fields=['course','stat'],
                name='unique course_stats',
            ),
        ]

class Like(models.Model):
    user                = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course              = models.ForeignKey('Course',on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'likes'
        constraints     = [
            models.UniqueConstraint(
                fields=['user','course'],
                name='unique likes',
            ),
        ]

class Category(models.Model):
    name                = models.CharField(max_length=30)
    
    class Meta:
        db_table        = 'categories'

class SubCategory(models.Model):
    name                = models.CharField(max_length=30)
    category            = models.ForeignKey('Category',on_delete=models.CASCADE)
    
    class Meta:
        db_table        = 'sub_categories'     