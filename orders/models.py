from django.db import models

# Create your models here.

class Pasta(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Salads(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name} - ${self.price}"

SIZES = (
    ('S', 'Small'),
    ('L', 'Large'),
)

class DinnerPlatters(models.Model):
    name = models.CharField(max_length=32)
    size = models.CharField(max_length=1, choices=SIZES)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name}({self.get_size_display()}) - ${self.price}"

class SubExtras(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Sub(models.Model):
    name = models.CharField(max_length=32)
    size = models.CharField(max_length=1, choices=SIZES)
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')
    extras = models.ManyToManyField(SubExtras, blank=True)

    def __str__(self):
        if self.extras.count() == 0:
            return f"{self.name}({self.get_size_display()}) - ${self.price} | No Extras"
        else:
            return f"{self.name}({self.get_size_display()}) - ${self.price} | Extras: {self.extras.in_bulk()}"

