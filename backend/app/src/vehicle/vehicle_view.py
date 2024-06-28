from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError
from app.src.vehicle.vehicle_logic import VehicleLogic


class VehicleAPIView(APIView):
    """
    API View to handle read, update, and delete operations for a vehicle.
    """

    @permission_classes([IsAuthenticated])
    def get(self, request: Request, license_plate: str = None) -> Response:
        """
        Retrieves the data of a specific vehicle.

        Args:
            request (Request): The HTTP request object.
            license_plate (str, optional): The license plate of the vehicle to retrieve. Default is None.

        Returns:
            Response: A response object with the vehicle's data on success or an error message on failure.
        """
        try:
            vehicle_util = VehicleLogic()
            data_out = vehicle_util.get_vehicle(license_plate)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def put(self, request: Request, license_plate: str = None) -> Response:
        """
        Modifies the data of a specific vehicle.

        Args:
            request (Request): The HTTP request object.
            license_plate (str, optional): The license plate of the vehicle to modify. Default is None.

        Returns:
            Response: A response object with the updated vehicle's data on success or an error message on failure.
        """
        try:
            vehicle_util = VehicleLogic()
            data_out = vehicle_util.modify_vehicle(license_plate, request.data)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidDataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def delete(self, request: Request, license_plate: str) -> Response:
        """
        Deletes a specific vehicle.

        Args:
            request (Request): The HTTP request object.
            license_plate (str): The license plate of the vehicle to delete.

        Returns:
            Response: A response object with a confirmation message on success or an error message on failure.
        """
        try:
            vehicle_util = VehicleLogic()
            vehicle_util.delete_vehicle(license_plate)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": 'ok'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class CreateVehicleAPIView(APIView):
    """
    API View to handle the creation of new vehicles.
    """

    def post(self, request: Request) -> Response:
        """
        Creates a new vehicle.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A response object with the created vehicle's data on success or an error message on failure.
        """
        vehicle_util = VehicleLogic()
        try:
            vehicle = vehicle_util.create_vehicle(request.data)
        except InvalidDataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": vehicle}, status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
class AllVehicleAPIView(APIView):
    """
    API View to handle the retrieval of all vehicles.
    """

    def get(self, request: Request) -> Response:
        """
        Retrieves the data of all vehicles.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A response object with the data of all vehicles on success or an error message on failure.
        """
        try:
            vehicle_util = VehicleLogic()
            data_out = vehicle_util.get_all_vehicles()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)
