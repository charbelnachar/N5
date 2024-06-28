from urllib.request import Request
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError
from app.src.person.person_logic import PersonLogic

@permission_classes([IsAuthenticated])
class PersonEmailAPIView(APIView):
    def get(self, request, email: str = None) -> Response:
        """
        Retrieves the details of a person by their email address.

        Args:
            request (Request): The HTTP request object.
            email (str, optional): The email address of the person to retrieve. Default is None.

        Returns:
            Response: A response object with the person's data on success.
                      On error, returns a response object with an error message and the corresponding HTTP status code.

        Raises:
            InvalidIdentifierError: If the provided email does not correspond to any person.
            Exception: If any other error occurs during the execution of the method.
        """
        person_util = PersonLogic()

        try:
            person = person_util.get_person_by_email(email)
            return Response(person, status=status.HTTP_200_OK)
        except InvalidIdentifierError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@permission_classes([IsAuthenticated])
class PersonAPIView(APIView):
    """
    API View to handle read, update, and delete operations for a person.
    """

    def get(self, request: Request, identifier: str = None) -> Response:
        """
        Retrieves the data of a specific person.

        Args:
            request (Request): The HTTP request object.
            identifier (str, optional): The identifier of the person to retrieve. Default is None.

        Returns:
            Response: A response object with the person's data on success or an error message on failure.
        """
        try:
            person_util = PersonLogic()
            data_out = person_util.get_person(identifier)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)

    def put(self, request: Request, identifier: str = None) -> Response:
        """
        Modifies the data of a specific person.

        Args:
            request (Request): The HTTP request object.
            identifier (str, optional): The identifier of the person to modify. Default is None.

        Returns:
            Response: A response object with the updated person's data on success or an error message on failure.
        """
        try:
            person_util = PersonLogic()
            data_out = person_util.modify_person(identifier, request.data)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)

    def delete(self, request: Request, identifier: str = None) -> Response:
        """
        Deletes a specific person.

        Args:
            request (Request): The HTTP request object.
            identifier (str, optional): The identifier of the person to delete. Default is None.

        Returns:
            Response: A response object with a confirmation message on success or an error message on failure.
        """
        try:
            person_util = PersonLogic()
            person_util.delete_person(identifier)
        except InvalidIdentifierError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": 'ok'}, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class CreatePersonAPIView(APIView):
    """
    API View to handle the creation of new persons.
    """

    def post(self, request: Request) -> Response:
        """
        Creates a new person.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A response object with the created person's data on success or an error message on failure.
        """
        person_util = PersonLogic()
        try:
            person = person_util.create_person(request.data)
        except InvalidDataError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": person}, status=status.HTTP_200_OK)



@permission_classes([IsAuthenticated])
class AllPersonAPIView(APIView):
    """
    API View to handle the retrieval of all persons.
    """

    def get(self, request: Request) -> Response:
        """
        Retrieves the data of all persons.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A response object with the data of all persons on success or an error message on failure.
        """
        try:
            person_util = PersonLogic()
            data_out = person_util.get_all_persons()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"data": data_out}, status=status.HTTP_200_OK)
