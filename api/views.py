import re
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Vehicle, Plate
from .serializers import VehicleDetailSerializer


def normalize_plate(plate_number):
    """Normalize plate number by removing spaces and converting to uppercase"""
    return re.sub(r"\s+", "", plate_number).upper()


@extend_schema(
    operation_id='health_check',
    summary='Проверка состояния API',
    description='Проверяет состояние API и подключение к базе данных',
    tags=['Health'],
    responses={
        200: {
            'description': 'API работает нормально',
            'examples': {
                'application/json': {
                    'ok': True,
                    'database': 'connected'
                }
            }
        },
        503: {
            'description': 'Проблемы с подключением к базе данных',
            'examples': {
                'application/json': {
                    'ok': True,
                    'database': 'not_connected'
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    try:
        # Test database connection
        Vehicle.objects.first()
        return Response({"ok": True, "database": "connected"})
    except Exception as e:
        return Response({"ok": True, "database": "not_connected"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@extend_schema(
    operation_id='list_plates',
    summary='Список номерных знаков',
    description='Возвращает список всех активных номерных знаков в системе',
    tags=['Plates'],
    responses={
        200: {
            'description': 'Список номерных знаков',
            'examples': {
                'application/json': {
                    'plates': ['123ABC02', '456DEF03', '789GHI04'],
                    'count': 3
                }
            }
        },
        500: {
            'description': 'Ошибка базы данных',
            'examples': {
                'application/json': {
                    'detail': 'db_error: DatabaseError: connection failed'
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def list_plates(request):
    """List all current plate numbers"""
    try:
        current_plates = Plate.objects.filter(released_at__isnull=True).order_by('plate_number')
        plates = [plate.plate_number for plate in current_plates]
        return Response({"plates": plates, "count": len(plates)})
    except Exception as e:
        return Response(
            {"detail": f"db_error: {type(e).__name__}: {e}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    operation_id='check_plate',
    summary='Проверка по номерному знаку',
    description='Возвращает полную информацию о транспортном средстве по номерному знаку, включая данные о владельце, водительском удостоверении, страховых полисах и авариях',
    tags=['Vehicles'],
    parameters=[
        OpenApiParameter(
            name='plate',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Номерной знак транспортного средства',
            examples=[
                OpenApiExample('Пример 1', value='123ABC02'),
                OpenApiExample('Пример 2', value='456DEF03'),
            ]
        )
    ],
    responses={
        200: {
            'description': 'Информация о транспортном средстве',
            'examples': {
                'application/json': {
                    'plate': '123ABC02',
                    'vehicle': {
                        'vehicle_id': 1,
                        'vin': 'WVWZZZ1JZXW000001',
                        'make': 'Volkswagen',
                        'model': 'Golf',
                        'year': 2019,
                        'color': 'white'
                    },
                    'owner': {
                        'owner_id': 1,
                        'full_name': 'Иванов Иван Иванович',
                        'iin': '900101123456',
                        'dob': '1990-01-01',
                        'phone': '+77010000000'
                    },
                    'driver_license': {
                        'license_id': 1,
                        'number': 'KZ1234567',
                        'categories': 'B,BE',
                        'issued_at': '2020-02-01',
                        'expires_at': '2030-02-01',
                        'status': 'valid'
                    },
                    'insurance': [
                        {
                            'policy_number': 'OSG-2025-0001',
                            'type': 'OSAGO',
                            'insurer': 'Jusan Insurance',
                            'valid_from': '2025-01-01',
                            'valid_to': '2025-12-31',
                            'status': 'active'
                        }
                    ],
                    'accidents': [
                        {
                            'accident_id': 1,
                            'date': '2024-05-10',
                            'severity': 'minor',
                            'location': 'Алматы',
                            'description': 'Столкновение на парковке',
                            'fault_party': 'other',
                            'damaged_parts': [
                                {
                                    'part_id': 1,
                                    'name': 'Передний бампер',
                                    'category': 'Кузов',
                                    'description': 'Передняя часть автомобиля'
                                },
                                {
                                    'part_id': 2,
                                    'name': 'Правое крыло',
                                    'category': 'Кузов',
                                    'description': 'Правое переднее крыло'
                                }
                            ]
                        }
                    ]
                }
            }
        },
        404: {
            'description': 'Номерной знак не найден',
            'examples': {
                'application/json': {
                    'detail': 'plate not found'
                }
            }
        },
        500: {
            'description': 'Ошибка базы данных',
            'examples': {
                'application/json': {
                    'detail': 'db_error: DatabaseError: connection failed'
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def check_plate(request, plate):
    """Check vehicle information by plate number"""
    try:
        plate_norm = normalize_plate(plate)
        
        # Find the vehicle with this plate number
        current_plate = Plate.objects.filter(
            plate_number__iexact=plate_norm,
            released_at__isnull=True
        ).select_related('vehicle', 'vehicle__owner').first()
        
        if not current_plate:
            return Response(
                {"detail": "plate not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        vehicle = current_plate.vehicle
        
        # Get owner information
        owner_data = None
        if vehicle.owner:
            owner_data = {
                'owner_id': vehicle.owner.owner_id,
                'full_name': vehicle.owner.full_name,
                'iin': vehicle.owner.iin,
                'dob': vehicle.owner.dob,
                'phone': vehicle.owner.phone
            }
        
        # Get driver license (latest one)
        driver_license_data = None
        if vehicle.owner:
            latest_license = vehicle.owner.driver_licenses.order_by('-expires_at').first()
            if latest_license:
                driver_license_data = {
                    'license_id': latest_license.license_id,
                    'number': latest_license.number,
                    'categories': latest_license.categories,
                    'issued_at': latest_license.issued_at,
                    'expires_at': latest_license.expires_at,
                    'status': latest_license.status
                }
        
        # Get insurance policies
        insurance_policies = []
        for policy in vehicle.insurance_policies.all():
            policy_data = {
                'policy_number': policy.policy_number,
                'type': policy.type,
                'insurer': policy.insurer.name if policy.insurer else None,
                'valid_from': policy.valid_from,
                'valid_to': policy.valid_to,
                'status': policy.status
            }
            insurance_policies.append(policy_data)
        
        # Get accidents (last 10)
        accidents = []
        for accident in vehicle.accidents.order_by('-date')[:10]:
            # Get damaged parts for this accident
            damaged_parts = []
            for part in accident.damaged_parts.all():
                part_data = {
                    'part_id': part.part_id,
                    'name': part.name,
                    'category': part.category,
                    'description': part.description
                }
                damaged_parts.append(part_data)
            
            accident_data = {
                'accident_id': accident.accident_id,
                'date': accident.date,
                'severity': accident.severity,
                'location': accident.location,
                'description': accident.description,
                'fault_party': accident.fault_party,
                'damaged_parts': damaged_parts
            }
            accidents.append(accident_data)
        
        # Build response
        result = {
            'plate': current_plate.plate_number,
            'vehicle': {
                'vehicle_id': vehicle.vehicle_id,
                'vin': vehicle.vin,
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'color': vehicle.color
            },
            'owner': owner_data,
            'driver_license': driver_license_data,
            'insurance': insurance_policies,
            'accidents': accidents
        }
        
        return Response(result)
        
    except Exception as e:
        return Response(
            {"detail": f"db_error: {type(e).__name__}: {e}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
