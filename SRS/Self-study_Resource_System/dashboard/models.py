from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

# notes section

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"
 
    def __str__(self):
        return self.title
    
# homework section
    
class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()

    # Homework document upload section

    document = models.FileField(upload_to='homework_documents/', blank=True, null=True)
    
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.document and os.path.isfile(self.document.path):
            os.remove(self.document.path)
        super().delete(*args, **kwargs)

#to do section

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

#groupstudy

class GroupStudy(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "group_creator")
    members = models.ManyToManyField(User,related_name="group_members",blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    

#ebooks

class Ebooks(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.TextField()
    document = models.FileField(upload_to='ebooks/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.document and os.path.isfile(self.document.path):
            os.remove(self.document.path)
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Ebooks"
        verbose_name_plural = "Ebooks"
    
    def __str__(self):
        return self.subject
    

class GroupHomework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupStudy, on_delete=models.CASCADE, null=True, blank=True, related_name='homeworks')
    subject = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due = models.DateField()
    document = models.FileField(upload_to='homework_documents/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.document and os.path.isfile(self.document.path):
            os.remove(self.document.path)
        super().delete(*args, **kwargs)






# class GroupStudy(models.Model):
#     name = models.CharField(max_length=255)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_created')
#     members = models.ManyToManyField(User, related_name='groups')