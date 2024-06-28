from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from app.models import Person, Vehicle, Officer, Violation
from app.src.exception.custom_exep import InvalidDataError

from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Officer


class PersonSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    name = serializers.CharField(allow_blank=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'email']
        read_only_fields = ['id']

    def validate_email(self, value):

        if self.instance:

            if Person.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise InvalidDataError(detail="El correo electrónico ya está en uso.", data={'email': value})
        else:

            if Person.objects.filter(email=value).exists():
                raise InvalidDataError(detail="El correo electrónico ya está en uso.", data={'email': value})

        return value

    def validate_name(self, value):
        print("Validating name")
        if not value.strip():
            raise InvalidDataError(detail="El nombre no puede estar vacío.", data={'name': value})
        return value
class VehicleSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(allow_blank=True)
    brand = serializers.CharField(allow_blank=True)
    color = serializers.CharField(allow_blank=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    # owner = serializers.CharField(allow_blank=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'license_plate', 'brand', 'color', 'owner']
        read_only_fields = ['id']

    def validate_license_plate(self, value):
        if not value.strip():
            raise InvalidDataError(detail="La placa del vehículo no puede estar vacía.", data={'license_plate': value})
        return value

    def validate_brand(self, value):
        if not value.strip():
            raise InvalidDataError(detail="La marca del vehículo no puede estar vacía.", data={'brand': value})
        return value

    def validate_color(self, value):
        if not value.strip():
            raise InvalidDataError(detail="El color del vehículo no puede estar vacío.", data={'color': value})
        return value

    def validate_owner(self, value):
        # if not value.strip():
        #     raise InvalidDataError(detail="El propietario del vehículo no puede estar vacío.", data={'owner': value})

        if value is None:
            raise serializers.ValidationError("El propietario especificado no existe.")
        if not Person.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("El propietario especificado no existe.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        owner_name = instance.owner.name
        owner_email = instance.owner.email
        owner_id = instance.owner.id
        representation['owner'] = {
            'id': owner_id,
            'name': owner_name,
            'email': owner_email
        }
        return representation

    def create(self, validated_data):
        license_plate = validated_data.get('license_plate')
        brand = validated_data.get('brand')
        color = validated_data.get('color')
        owner = validated_data.get('owner')

        # Validaciones adicionales si es necesario
        if Vehicle.objects.filter(license_plate=license_plate).exists():
            raise InvalidDataError(detail="El vehículo con esta placa ya existe.",
                                   data={'license_plate': license_plate})

        vehicle = Vehicle.objects.create(
            license_plate=license_plate,
            brand=brand,
            color=color,
            owner=owner
        )
        return vehicle

    def update(self, instance, validated_data):
        if 'license_plate' in validated_data:
            raise InvalidDataError(detail="No se puede modificar la placa del vehículo.",
                                   data={'license_plate': validated_data['license_plate']})

        instance.brand = validated_data.get('brand', instance.brand)
        instance.color = validated_data.get('color', instance.color)
        if 'owner' in validated_data:
            owner = validated_data['owner']
            if not Person.objects.filter(id=owner.id).exists():
                raise InvalidDataError(detail="El propietario especificado no existe.",
                                       data={'owner': owner.id})
            instance.owner = owner

        instance.save()
        return instance

    def __str__(self):
        return (
            f"Vehicle: id={self.instance.id}, license_plate={self.instance.license_plate}, brand={self.instance.brand},"
            f" color={self.instance.color}, owner={self.instance.owner.name} ({self.instance.owner.email})")



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class OfficerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email', required=False)
    password = serializers.CharField(source='user.password', write_only=True, required=False ,allow_blank=True)
    identifier = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Officer
        fields = ['username', 'email', 'password', 'name', 'identifier']
        read_only_fields = ['id', 'identifier']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = {
            'username': instance.user.username,
            'name': instance.name,
            'email': instance.user.email,
            'identifier': instance.identifier
        }
        return representation

    def validate_identifier(self, value):
        if self.instance and self.instance.identifier != value:
            if Officer.objects.filter(identifier=value).exists():
                raise InvalidDataError(detail="El identificador ya existe", data={'identifier': value})
        return value

    def validate_username(self, value):
        if self.instance and self.instance.user.username != value:
            if User.objects.filter(username=value).exists():
                raise InvalidDataError(detail="El nombre de usuario ya existe", data={'username': value})
        return value

    def validate(self, data):
        if 'password' in data and not data['password']:
            data.pop('password')
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        username = user_data['username']
        password = make_password(user_data['password']) if 'password' in user_data else None
        user_data['password'] = password

        if User.objects.filter(username=username).exists():
            raise InvalidDataError(detail="El nombre de usuario ya existe", data={'username': username})

        user = User.objects.create_user(**user_data)
        officer = Officer.objects.create(user=user, **validated_data)
        return officer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            if 'username' in user_data and User.objects.filter(username=user_data['username']).exclude(pk=instance.user.pk).exists():
                raise InvalidDataError(detail="El nombre de usuario ya existe", data={'username': user_data['username']})

            for attr, value in user_data.items():
                if attr == 'password' and value:  # Only update password if it's provided
                    instance.user.set_password(value)
                elif attr != 'password':  # Update other fields
                    setattr(instance.user, attr, value)
            instance.user.save()

        if 'identifier' in validated_data:
            if Officer.objects.filter(identifier=validated_data['identifier']).exclude(pk=instance.pk).exists():
                raise InvalidDataError(detail="El identificador ya existe", data={'identifier': validated_data['identifier']})

        if 'identifier' in validated_data and validated_data['identifier'] != instance.identifier:
            raise InvalidDataError(detail="El identificador no puede ser modificado", data={'identifier': validated_data['identifier']})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# class OfficerSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username')
#     password = serializers.CharField(source='user.password', write_only=True, required=False)
#
#     email = serializers.CharField(source='user.email', required=False)
#     identifier = serializers.CharField(write_only=True, required=False)
#
#     class Meta:
#         model = Officer
#         fields = ['username','email',  'password', 'name', 'identifier']
#         read_only_fields = ['id', 'identifier']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#
#         representation = {
#             'username': instance.user.username,
#             'name': instance.name,
#             'email': instance.user.email,
#             'identifier' : instance.identifier
#         }
#         return representation
#
#
#     def validate_identifier(self, value):
#         if self.instance and self.instance.identifier != value:
#             if Officer.objects.filter(identifier=value).exists():
#                 raise InvalidDataError(detail="El identificador ya existe", data={'identifier': value})
#         return value
#
#     def validate_username(self, value):
#         if self.instance and self.instance.user.username != value:
#             if User.objects.filter(username=value).exists():
#                 raise InvalidDataError(detail="El nombre de usuario ya existe", data={'username': value})
#         return value
#
#
#     def validate(self, data):
#         if 'password' in data and not data['password']:
#             data.pop('password')
#
#         if 'password' in data and data.get('password') != data.get('confirm_password'):
#             raise serializers.ValidationError("Las contraseñas no coinciden.")
#         return data
#
#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         username = user_data['username']
#         password = make_password(user_data['password'])
#         user_data['password'] = password
#
#
#         if User.objects.filter(username=username).exists():
#             raise InvalidDataError(detail="El nombre de Oficial ya existe", data={'username': username})
#
#
#         user = User.objects.create_user(**user_data)
#         officer = Officer.objects.create(user=user, **validated_data)
#         return officer
#
#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', None)
#         if user_data:
#             if 'username' in user_data and User.objects.filter(username=user_data['username']).exclude(pk=instance.user.pk).exists():
#                 raise InvalidDataError(detail="El nombre de Oficial ya existe", data={'username': user_data['username']})
#
#             for attr, value in user_data.items():
#                 setattr(instance.user, attr, value)
#             instance.user.save()
#
#         if 'identifier' in validated_data:
#             if Officer.objects.filter(identifier=validated_data['identifier']).exclude(pk=instance.pk).exists():
#                 raise InvalidDataError(detail="El identificador ya existe", data={'identifier': validated_data['identifier']})
#
#         if validated_data['identifier'] != instance.identifier:
#             raise InvalidDataError(detail="El identificador no puede ser modificado",
#                                    data={'identifier': validated_data['identifier']})
#
#         for attr, value in validated_data.items():
#             if attr != 'password':  # Skip password update here
#                 setattr(instance, attr, value)
#             else:
#                 if value:  # Only update password if it's provided
#                     instance.user.set_password(value)
#
#         # for attr, value in validated_data.items():
#         #     setattr(instance, attr, value)
#         instance.save()
#         return instance
#

class ViolationSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(write_only=True)
    vehicle = VehicleSerializer(read_only=True)

    class Meta:
        model = Violation
        fields = ['id', 'license_plate', 'vehicle', 'officer', 'timestamp', 'comments']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if isinstance(instance, Violation):
            officer_name = instance.officer.name if instance.officer else None
            officer_id = instance.officer.id if instance.officer else None
            vehicle_id = instance.vehicle.id
            license_plate = instance.vehicle.license_plate
        else:

            officer_name = instance['officer'].name if instance['officer'] else None
            officer_id = instance['officer'].id if instance['officer'] else None
            vehicle_id = instance['license_plate'].id
            license_plate = instance['license_plate'].license_plate

        # Obtener detalles del vehículo
        if vehicle_id and license_plate:
            vehicle_id = vehicle_id
            license_plate = license_plate
        else:
            vehicle_id = None
            license_plate = None

        # Añadir detalles a la representación
        representation['vehicle'] = {
            'id': vehicle_id,
            'license_plate': license_plate,
        }
        representation['officer'] = {
            'id': officer_id,
            'name': officer_name,
        }
        return representation



    def validate_officer(self, value):
        if not value:
            raise serializers.ValidationError("El Oficial con este id no existe.")
        return value

    def validate_license_plate(self, value):
        try:
            value = Vehicle.objects.get(license_plate=value)
        except Vehicle.DoesNotExist:
            raise InvalidDataError(detail="El vehículo con esta placa no existe.",
                                   data={'Vehicle': value})

        return value

    def create(self, validated_data):
        # license_plate = validated_data.pop('license_plate')
        # vehicle = Vehicle.objects.get(license_plate=license_plate)
        officer_instance = validated_data.get('officer')

        # officer_instance = Officer.objects.get(user_id=officer)

        # violation = Violation.objects.create(vehicle=validated_data, officer=officer_instance, **validated_data)
        violation = Violation()
        violation.vehicle = validated_data['license_plate']
        violation.officer = validated_data['officer']
        violation.timestamp = validated_data['timestamp']
        violation.comments = validated_data['comments']
        violation.save()
        return violation

    def update(self, instance, validated_data):
        if 'vehicle' in validated_data:
            raise InvalidDataError(detail="No se puede modificar el vehículo",
                                   data={'vehicle': validated_data['vehicle']})
        if 'officer' in validated_data:
            raise InvalidDataError(detail="No se puede modificar el oficial",
                                   data={'officer': validated_data['officer']})

        if 'timestamp' in validated_data:
            instance.timestamp = validated_data['timestamp']
        if 'comments' in validated_data:
            instance.comments = validated_data['comments']

        instance.save()
        return instance




