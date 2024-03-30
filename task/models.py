from django.db import models

# Create your models here.
class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True, null=False)
    task_content = models.CharField(max_length=300, null=False)
    task_date = models.DateField(null=False, auto_now_add=True)