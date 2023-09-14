from django.db import models, migrations
from django.utils.text import slugify
from users.models import Profile
from uuid import uuid4
import uuid
from simple_history.models import HistoricalRecords

# Create your models here.
# def convert_int_to_uuid(apps, schema_editor):
#     YourModel = apps.get_model('food', 'LunchMeal')
#
#     for item in YourModel.objects.all():
#         # Convert the integer ID to a hexadecimal string and pad it with zeros
#         hex_id = format(item.id, '032x')
#
#         # Cast the hexadecimal string to UUID
#         item.id = uuid.UUID(hex_id)
#         item.save()
#
# class Migration(migrations.Migration):
#
#     dependencies = [
#         ('food', '0013_historicallunchmenuoption.py'),
#     ]
#
#     operations = [
#         migrations.RunPython(convert_int_to_uuid),
#     ]
class PizzaDayDay(models.Model):
    to_date = models.DateField(auto_now_add=False)
    slug = models.SlugField(blank=True, null=True)
    registration_open = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Vytvoření slugu z data
            self.slug = slugify(str(self.to_date))
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.to_date)

class PizzaOrder(models.Model):
    ordered_by = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=False, null=False)
    TIME_CHOICES = [
        ('10:00', '10:00'),
        ('10:45', '10:45'),
        ('12:00', '12:00'),
        ('17:45', '17:45'),
        ('18:30', '18:30'),
    ]
    to_time = models.CharField(max_length=5, choices=TIME_CHOICES, blank=True, null=True)

    PIZZA_CHOICES = [
        ('hawai', 'hawai'),
        ('funghi', 'funghi'),
        ('salami', 'salami'),
        ('ham & chicken', 'ham & chicken'),
        ('quattro formaggi', 'quattro formaggi'),
        ('deviola', 'deviola'),
        ('olives', 'olives'),
        ("doesn't matter which pizza", "doesn't matter which pizza"),
    ]
    selection = models.CharField(max_length=26, choices=PIZZA_CHOICES, blank=True, null=True)
    pizza_day = models.ForeignKey(PizzaDayDay, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"{self.pizza_day} {self.ordered_by} {self.to_time} {self.selection}"

class LunchMeal(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=2000, blank=True, null=True)
    image = models.ImageField(upload_to='meals', default="meals/default.png")
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.price}"

class LunchMenu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"{self.date}"
#UPDEJTOVAT
class LunchMenuOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    meal = models.ForeignKey(LunchMeal, on_delete=models.SET_NULL, null=True)
    menu = models.ForeignKey(LunchMenu, on_delete=models.CASCADE)
    available_portions = models.IntegerField()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Pokud meal byl smazán, nastavte výchozí hodnotu
        if not self.meal:
            self.meal = "meal deleted"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.meal} {self.menu}"

class LunchOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4,  editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    menu_option = models.ForeignKey(LunchMenuOption, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Pokud meal byl smazán, nastavte výchozí hodnotu
        if not self.menu_option:
            self.menu_option = "menu option deleted"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} {self.menu_option} {self.ordered_at}"

class TransactionHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    transaction = models.CharField(max_length=200, blank=False, null=False)
    related_user = models.CharField(max_length=200, blank=False, null=False)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} {self.related_user} {self.value} {self.transaction}"



