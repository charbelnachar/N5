from urllib.request import Request

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError
from app.src.officer.officer_logic import OfficerLogic

class OfficerAPIView(APIView):
    """
    API View to handle read, update, and delete operations for an officer.
    """

    def get(self, request: Request, identifier: str = None) -> Response:
        """
        Retrieves the data of a specific officer.

        Args:
            request (Request): The HTTP request object.
            identifier (str, optional): The identifier of the officer to retrieve. Default is None.

        Returns:
            Response: A response object with the officer's data on success or an error message on failure.
        """
        try:
            officer_util = OfficerLogic()
            data_out = officer_util.get_officer(identifier)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)

    def put(self, request: Request, identifier: str = None) -> Response:
        """
        Modifies the data of a specific officer.

        Args:
            request (Request): The HTTP request object.
            identifier (str, optional): The identifier of the officer to modify. Default is None.

        Returns:
            Response: A response object with the updated officer's data on success or an error message on failure.
        """
        try:
            officer_util = OfficerLogic()
            data_out = officer_util.modify_officer(identifier, request.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)

    def delete(self, request: Request, identifier: str = None) -> Response:
        """
        Deletes a specific officer.

        Args:
            request (Request): The HTTP request object.
            identifier (str, optional): The identifier of the officer to delete. Default is None.

        Returns:
            Response: A response object with a confirmation message on success or an error message on failure.
        """
        try:
            officer_util = OfficerLogic()
            officer_util.delete_officer(identifier)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": 'ok'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class CreateOfficerAPIView(APIView):
    """
    API View to handle the creation of new officers.
    """

    def post(self, request: Request) -> Response:
        """
        Creates a new officer.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A response object with the created officer's data on success or an error message on failure.
        """
        officer_util = OfficerLogic()
        try:
            print(request.data)
            officer = officer_util.create_officer(request.data)
        except InvalidDataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": officer}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class AllOfficerAPIView(APIView):
    """
    API View to handle the retrieval of all officers.
    """

    def get(self, request: Request) -> Response:
        """
        Retrieves the data of all officers.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A response object with the data of all officers on success or an error message on failure.
        """
        try:
            officer_util = OfficerLogic()
            data_out = officer_util.get_all_officers()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)
