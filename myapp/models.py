from django.db import models

# Create your models here.
class Predictions(models.Model):
    Symptoms = models.CharField(max_length=500)
    Conditions = models.CharField(max_length=20)
    Confidence = models.FloatField()
    RecommendedDrug = models.CharField(max_length=50)
    Pre_Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Predictionss"