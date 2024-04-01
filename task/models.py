from datetime import date

from django.db import models


class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True, null=False)
    task_content = models.CharField(max_length=300, null=False)
    task_date = models.DateField(null=False, default=date.today)
