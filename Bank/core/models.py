from django.db import models

class BankRuft(models.Model):
    name=models.CharField(max_length=20,null=True)
    bankruft=models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.name)} "
        