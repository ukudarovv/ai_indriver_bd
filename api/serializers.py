from rest_framework import serializers
from .models import Owner, DriverLicense, Vehicle, Plate, Insurer, InsurancePolicy, Accident, CarPart


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['owner_id', 'full_name', 'iin', 'dob', 'phone']


class DriverLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLicense
        fields = ['license_id', 'number', 'categories', 'issued_at', 'expires_at', 'status']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'vin', 'make', 'model', 'year', 'color']


class PlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plate
        fields = ['plate_id', 'plate_number', 'region', 'assigned_at', 'released_at']


class InsurerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = ['insurer_id', 'name']


class InsurancePolicySerializer(serializers.ModelSerializer):
    insurer_name = serializers.CharField(source='insurer.name', read_only=True)
    
    class Meta:
        model = InsurancePolicy
        fields = ['policy_id', 'policy_number', 'type', 'insurer_name', 'valid_from', 'valid_to', 'status']


class CarPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPart
        fields = ['part_id', 'name', 'category', 'description']


class AccidentSerializer(serializers.ModelSerializer):
    damaged_parts = CarPartSerializer(many=True, read_only=True)
    
    class Meta:
        model = Accident
        fields = ['accident_id', 'date', 'severity', 'location', 'description', 'fault_party', 'damaged_parts']


class VehicleDetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    current_plate = serializers.SerializerMethodField()
    driver_license = serializers.SerializerMethodField()
    insurance_policies = InsurancePolicySerializer(many=True, read_only=True)
    accidents = AccidentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'vin', 'make', 'model', 'year', 'color', 'owner', 
                 'current_plate', 'driver_license', 'insurance_policies', 'accidents']
    
    def get_current_plate(self, obj):
        current_plate = obj.plates.filter(released_at__isnull=True).first()
        if current_plate:
            return current_plate.plate_number
        return None
    
    def get_driver_license(self, obj):
        if obj.owner:
            latest_license = obj.owner.driver_licenses.order_by('-expires_at').first()
            if latest_license:
                return DriverLicenseSerializer(latest_license).data
        return None
