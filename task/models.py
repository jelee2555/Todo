from datetime import date

from django.db import models


class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True, null=False)
    task_content = models.CharField(max_length=300, null=False)
    task_date = models.DateField(null=False, default=date.today)
    user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='id', db_column='user_id')
