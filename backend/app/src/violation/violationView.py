from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.src.violation.violation_logic import ViolationLogic
from app.src.exception.custom_exep import InvalidDataError, InvalidIdentifierError


class ReportViolationView(APIView):
    """
    API View to handle reporting violations for a specific person.
    """

    def get(self, request):
        """
        Retrieves violations for a person based on their email.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response object with the violations data on success or an error message on failure.
        """
        email = request.GET.get('email',None)
        violation_logic = ViolationLogic()

        try:
            violation_data = violation_logic.get_violations_by_email(email)
            return Response(violation_data, status=status.HTTP_200_OK)
        except InvalidDataError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidIdentifierError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class ViolationAPIView(APIView):
    """
    API View to handle CRUD operations for violations.
    """

    def get(self, request, violation_id=None):
        """
        Retrieves a specific violation or all violations.

        Args:
            request: The HTTP request object.
            violation_id (int, optional): The ID of the violation to retrieve. Default is None.

        Returns:
            Response: A response object with the violation(s) data on success or an error message on failure.
        """
        violation_logic = ViolationLogic()
        try:
            if violation_id:
                data = violation_logic.get_violation(violation_id)
            else:
                data = violation_logic.get_all_violations()
            return Response(data, status=status.HTTP_200_OK)
        except InvalidIdentifierError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, violation_id):
        """
        Updates a specific violation.

        Args:
            request: The HTTP request object.
            violation_id (int): The ID of the violation to update.

        Returns:
            Response: A response object with the updated violation's data on success or an error message on failure.
        """
        violation_logic = ViolationLogic()
        try:
            data = violation_logic.update_violation(violation_id, request.data)
            return Response(data, status=status.HTTP_200_OK)
        except InvalidIdentifierError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidDataError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, violation_id):
        """
        Deletes a specific violation.

        Args:
            request: The HTTP request object.
            violation_id (int): The ID of the violation to delete.

        Returns:
            Response: A response object with a success message on success or an error message on failure.
        """
        violation_logic = ViolationLogic()
        try:
            violation_logic.delete_violation(violation_id)
            return Response({'message': 'Infraccion eliminada'}, status=status.HTTP_200_OK)
        except InvalidIdentifierError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class CreateViolationView(APIView):
    """
    API View to handle creating a new violation.
    """

    def post(self, request):
        """
        Creates a new violation.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response object with the created violation's data on success or an error message on failure.
        """
        violation_logic = ViolationLogic()
        try:
            data = violation_logic.create_violation(request.data, request.user)
            return Response(data, status=status.HTTP_201_CREATED)
        except InvalidDataError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidIdentifierError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@permission_classes([IsAuthenticated])
class GetAllViolationAPIView(APIView):
    """
    API View to handle CRUD operations for violations.
    """

    def get(self, request):
        """
        Retrieves a specific violation or all violations.

        Args:
            request: The HTTP request object.
            violation_id (int, optional): The ID of the violation to retrieve. Default is None.

        Returns:
            Response: A response object with the violation(s) data on success or an error message on failure.
        """
        violation_logic = ViolationLogic()
        try:

            data = violation_logic.get_all_violations()
            return Response(data, status=status.HTTP_200_OK)
        except InvalidIdentifierError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
