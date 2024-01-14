from django.db import models


class Height_groups(models.Model):

    def __str__(self) -> str:
        return str(self.height_cm)

    height_cm = models.FloatField(null=False,blank=False)
    ht_per = models.FloatField(null=False,blank=False)


class Age_ref(models.Model):

    def __str__(self) -> str:
        return f'{self.age} - {int(self.age) + 4}' 

    age = models.CharField(max_length=5, null=False,blank=False)
    age_group_pop = models.IntegerField(null=False, blank=False)
    # age_rat= models.FloatField(null=False,blank=False)
    n_yet_married = models.FloatField(null=False,blank=False)
    married_num = models.FloatField(null=False,blank=False)
    n_married_num = models.FloatField(null=False,blank=False)
    is_obese_rate = models.FloatField(null=False,blank=False)
    not_obese_rate = models.FloatField(null=False,blank=False)
    smoke_rate = models.FloatField(null=False, blank=False)
    not_smoke_rate = models.FloatField(null=False, blank=False)
    
class Income_groups(models.Model):
    def __str__(self) -> str:
        return f'{self.age_group.age} - {self.income_yr}'

    age_group = models.ForeignKey(Age_ref, on_delete=models.CASCADE, related_name='income_groups') 
    income_yr = models.IntegerField(null=False,blank=False)
    income_ratio = models.FloatField(null=False,blank=False)