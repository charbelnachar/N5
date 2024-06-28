from rest_framework.exceptions import ValidationError

from app.models import Vehicle, Person
from app.src.serializer.serializers import VehicleSerializer
from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError
from app.src.utility.util_data import UtilData


class VehicleLogic:
    """
    Logic class for handling operations related to Vehicle.
    """

    def get_vehicle(self, license_plate: str) -> dict:
        """
        Retrieves a vehicle's data based on the given license plate.

        Args:
            license_plate (str): The license plate of the vehicle to retrieve.

        Returns:
            dict: The serialized data of the vehicle.

        Raises:
            InvalidIdentifierError: If the vehicle with the given license plate does not exist.
        """
        try:
            vehicle = Vehicle.objects.get(license_plate=license_plate)
        except Vehicle.DoesNotExist:
            raise InvalidIdentifierError(license_plate, "Vehicle does not exist")

        serializer = VehicleSerializer(vehicle)
        return serializer.data

    def get_all_vehicles(self) -> list:
        """
        Retrieves the data of all vehicles.

        Returns:
            list: A list of serialized data of all vehicles.
        """
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return serializer.data

    def modify_vehicle(self, license_plate: str, data: dict) -> dict:
        """
        Modifies the data of a specific vehicle.

        Args:
            license_plate (str): The license plate of the vehicle to modify.
            data (dict): The data to update the vehicle with.

        Returns:
            dict: The serialized data of the updated vehicle.

        Raises:
            InvalidIdentifierError: If the vehicle with the given license plate does not exist.
        """
        try:
            vehicle = Vehicle.objects.get(license_plate=license_plate)
            vehicle.license_plate = data.get('license_plate')
            vehicle.color = data.get('color')
            vehicle.brand = data.get('brand')
            vehicle.owner = Person.objects.get(id=data.get('owner'))
            vehicle.save()
        except Vehicle.DoesNotExist:
            raise InvalidDataError(detail="El Vehiculo no existe", data={'license_plate': license_plate})
        except Person.DoesNotExist:
            raise InvalidDataError(detail="El propietario no existe", data={'owner': data.get('owner')})
        except ValidationError as e:
            raise InvalidDataError(detail="Error de validacion", data=e.detail)
        return VehicleSerializer(vehicle).data
    def delete_vehicle(self, license_plate: str) -> None:
        """
        Deletes a specific vehicle.

        Args:
            license_plate (str): The license plate of the vehicle to delete.

        Returns:
            None

        Raises:
            InvalidIdentifierError: If the vehicle with the given license plate does not exist.
        """
        try:
            vehicle = Vehicle.objects.get(license_plate=license_plate)
            vehicle.delete()
        except Vehicle.DoesNotExist:
            raise InvalidIdentifierError(license_plate, "Vehicle does not exist")

    def create_vehicle(self, data: dict) -> dict:
        """
        Creates a new vehicle.

        Args:
            data (dict): The data to create the vehicle with.

        Returns:
            dict: The serialized data of the created vehicle.

        Raises:
            InvalidDataError: If the provided data is invalid.
       """
        UtilData.validate_dict_values(data)
        if Vehicle.objects.filter(license_plate=data['license_plate']).exists():
            raise InvalidDataError(detail="El vehiculo con esta placa ya existe.",
                                   data={'license_plate': data['license_plate']})

        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            print(serializer.errors)