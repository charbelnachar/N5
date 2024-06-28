from app.models import Person, Violation, Vehicle, Officer
from app.src.serializer.serializers import ViolationSerializer
from app.src.exception.custom_exep import InvalidDataError, InvalidIdentifierError
from app.src.utility.util_email import EmailValidator


class ViolationLogic:
    """
    Logic class for handling operations related to Violations.
    """

    def get_violations_by_email(self, email: str) -> list:
        """
        Retrieves violations for a person based on their email.

        Args:
            email (str): The email of the person whose violations to retrieve.

        Returns:
            list: A list of serialized violation data.

        Raises:
            InvalidDataError: If the provided email is invalid.
            InvalidIdentifierError: If no person is found with the given email.
        """

        EmailValidator.validate_email_format(email)

        try:
            person = Person.objects.get(email=email)
        except Person.DoesNotExist:
            raise InvalidDataError(detail="La persona de ese correo no exite", data={'email': email})

        violations = Violation.objects.filter(vehicle__owner=person)
        violation_data = ViolationSerializer(violations, many=True).data

        return violation_data

    def create_violation(self, data: dict, user) -> dict:
        """
        Creates a new violation.

        Args:
            data (dict): The data to create the violation with.
            user: The user creating the violation (should be an officer).

        Returns:
            dict: The serialized data of the created violation.

        Raises:
            InvalidDataError: If the provided data is invalid.
            InvalidIdentifierError: If the vehicle or officer is not found.
        """

        data['officer'] = user.id

        serializer = ViolationSerializer(data=data)
        if not serializer.is_valid():
            raise InvalidDataError(serializer.errors, "Invalid violation data provided")
        serializer.save()



        return serializer.data

    def get_violation(self, violation_id: int) -> dict:
        """
        Retrieves a specific violation.

        Args:
            violation_id (int): The ID of the violation to retrieve.

        Returns:
            dict: The serialized data of the violation.

        Raises:
            InvalidIdentifierError: If the violation with the given ID does not exist.
        """
        try:
            violation = Violation.objects.get(id=violation_id)
        except Violation.DoesNotExist:
            raise InvalidIdentifierError(violation_id, "Violation does not exist")

        return ViolationSerializer(violation).data

    def get_all_violations(self) -> list:
        """
        Retrieves all violations.

        Returns:
            list: A list of serialized data of all violations.
        """
        violations = Violation.objects.all()
        return ViolationSerializer(violations, many=True).data

    def update_violation(self, violation_id: int, data: dict) -> dict:
        """
        Updates a specific violation.

        Args:
            violation_id (int): The ID of the violation to update.
            data (dict): The data to update the violation with.

        Returns:
            dict: The serialized data of the updated violation.

        Raises:
            InvalidIdentifierError: If the violation with the given ID does not exist.
            InvalidDataError: If the provided data is invalid.
        """
        try:
            violation = Violation.objects.get(id=violation_id)
        except Violation.DoesNotExist:
            raise InvalidIdentifierError(violation_id, "Violation does not exist")

        serializer = ViolationSerializer(violation, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise InvalidDataError(data, "Invalid violation data provided")

    def delete_violation(self, violation_id: int) -> None:
        """
        Deletes a specific violation.

        Args:
            violation_id (int): The ID of the violation to delete.

        Raises:
            InvalidIdentifierError: If the violation with the given ID does not exist.
        """
        try:
            violation = Violation.objects.get(id=violation_id)
            violation.delete()
        except Violation.DoesNotExist:
            raise InvalidIdentifierError(violation_id, "Violation does not exist")
