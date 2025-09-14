from django.db import models
from django.core.validators import RegexValidator


class Owner(models.Model):
    owner_id = models.BigAutoField(primary_key=True)
    full_name = models.TextField()
    iin = models.CharField(max_length=12, unique=True, validators=[
        RegexValidator(regex=r'^\d{12}$', message='IIN must be 12 digits')
    ])
    dob = models.DateField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'owners'

    def __str__(self):
        return self.full_name


class DriverLicense(models.Model):
    STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('suspended', 'Suspended'),
        ('revoked', 'Revoked'),
        ('expired', 'Expired'),
    ]

    license_id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='driver_licenses')
    number = models.TextField(unique=True)
    categories = models.TextField()
    issued_at = models.DateField()
    expires_at = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'driver_licenses'

    def __str__(self):
        return f"{self.number} ({self.owner.full_name})"


class Vehicle(models.Model):
    vehicle_id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')
    vin = models.CharField(max_length=17, unique=True, validators=[
        RegexValidator(regex=r'^[A-HJ-NPR-Z0-9]{17}$', message='Invalid VIN format')
    ])
    make = models.TextField(null=True, blank=True)
    model = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    color = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'vehicles'

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - {self.vin}"


class Plate(models.Model):
    plate_id = models.BigAutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='plates')
    plate_number = models.TextField()
    region = models.TextField(null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'plates'
        constraints = [
            models.UniqueConstraint(
                fields=['plate_number', 'released_at'],
                name='uq_active_plate'
            )
        ]

    def __str__(self):
        return f"{self.plate_number} ({self.vehicle})"


class Insurer(models.Model):
    insurer_id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)

    class Meta:
        db_table = 'insurers'

    def __str__(self):
        return self.name


class InsurancePolicy(models.Model):
    TYPE_CHOICES = [
        ('OSAGO', 'OSAGO'),
        ('KASKO', 'KASKO'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    policy_id = models.BigAutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='insurance_policies')
    insurer = models.ForeignKey(Insurer, on_delete=models.SET_NULL, null=True, blank=True)
    policy_number = models.TextField(unique=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'insurance_policies'

    def __str__(self):
        return f"{self.policy_number} ({self.type})"


class CarPart(models.Model):
    """Модель для деталей автомобиля"""
    part_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, help_text="Название детали")
    category = models.CharField(max_length=50, help_text="Категория детали")
    description = models.TextField(null=True, blank=True, help_text="Описание детали")

    class Meta:
        db_table = 'car_parts'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class Accident(models.Model):
    FAULT_CHOICES = [
        ('owner', 'Owner'),
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ]
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('total', 'Total'),
    ]

    accident_id = models.BigAutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='accidents')
    date = models.DateField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    fault_party = models.CharField(max_length=10, choices=FAULT_CHOICES, default='unknown')
    damaged_parts = models.ManyToManyField(CarPart, blank=True, related_name='accidents', help_text="Поврежденные детали")

    class Meta:
        db_table = 'accidents'

    def __str__(self):
        return f"Accident {self.accident_id} - {self.vehicle} ({self.date})"
