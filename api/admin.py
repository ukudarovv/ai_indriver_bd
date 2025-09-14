from django.contrib import admin
from .models import Owner, DriverLicense, Vehicle, Plate, Insurer, InsurancePolicy, Accident


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['owner_id', 'full_name', 'iin', 'dob', 'phone']
    search_fields = ['full_name', 'iin', 'phone']


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ['license_id', 'number', 'owner', 'categories', 'issued_at', 'expires_at', 'status']
    list_filter = ['status', 'categories']
    search_fields = ['number', 'owner__full_name']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_id', 'vin', 'make', 'model', 'year', 'color', 'owner']
    search_fields = ['vin', 'make', 'model', 'owner__full_name']
    list_filter = ['make', 'year', 'color']


@admin.register(Plate)
class PlateAdmin(admin.ModelAdmin):
    list_display = ['plate_id', 'plate_number', 'vehicle', 'region', 'assigned_at', 'released_at']
    search_fields = ['plate_number', 'vehicle__vin']
    list_filter = ['region', 'assigned_at']


@admin.register(Insurer)
class InsurerAdmin(admin.ModelAdmin):
    list_display = ['insurer_id', 'name']
    search_fields = ['name']


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_id', 'policy_number', 'type', 'vehicle', 'insurer', 'valid_from', 'valid_to', 'status']
    list_filter = ['type', 'status', 'insurer']
    search_fields = ['policy_number', 'vehicle__vin']


@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = ['accident_id', 'vehicle', 'date', 'severity', 'location', 'fault_party']
    list_filter = ['severity', 'fault_party', 'date']
    search_fields = ['vehicle__vin', 'location', 'description']
