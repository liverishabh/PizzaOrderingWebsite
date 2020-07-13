from django.db import models

class Pasta(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name}"

class Salads(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name}"

class DinnerPlatters(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=5, decimal_places=2, help_text='Price in US dollars')
    price_large = models.DecimalField(max_digits=5, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name}"

class SubExtras(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Sub(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')
    price_large = models.DecimalField(max_digits=4, decimal_places=2, help_text='Price in US dollars')
    extras = models.ManyToManyField(SubExtras, blank=True)

    def __str__(self):
        return f"{self.name}"

class Toppings(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

STYLES = (
    ('R', 'Regular'),
    ('S', 'Sicilian')
)

class Pizza(models.Model):
    name = models.CharField(max_length=32)
    style = models.CharField(max_length=1, choices=STYLES)
    price_small = models.DecimalField(max_digits=5, decimal_places=2, help_text='Price in US dollars')
    price_large = models.DecimalField(max_digits=5, decimal_places=2, help_text='Price in US dollars')
    toppings = models.ManyToManyField(Toppings, blank=True)

    def __str__(self):
        return f"{self.get_style_display()} | {self.name}"

class Orders(models.Model):
    username = models.CharField(max_length=32)
    dishtype = models.CharField(max_length=32)
    dishname = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text='Price in US dollars')
    remarks = models.TextField()
    status = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.username} | {self.dishtype} ({self.dishname}) | {self.status}"

