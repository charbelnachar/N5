import re

from app.src.exception.custom_exep import InvalidDataError

class EmailValidator:
    @staticmethod
    def validate_email_format(email: str) -> None:
        """
        Validates if an email has the correct format.

        Args:
            email (str): The email to validate.

        Raises:
            InvalidDataError: If the email does not have a valid format.

        Returns:
            None
        """
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_regex, email):
            raise InvalidDataError(detail="Ingrese una dirección de correo electrónico válida.",
                                   data={'email': email})

