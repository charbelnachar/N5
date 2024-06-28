from app.src.exception.custom_exep import InvalidDataError

class UtilData:
    @staticmethod
    def validate_dict_values(data: dict):
        """
        Validates that none of the values in a dictionary are None or empty strings.

        Args:
            data (dict): The dictionary to validate.

        Raises:
            InvalidDataError: If a value is None or an empty string.
        """
        for key, value in data.items():
            if value is None or value == '':
                raise InvalidDataError(detail=f"El campo no puede estar vacío.", data={key: value})
