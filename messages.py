
class AuthMessages:
    INVALID_CREDENTIALS = "email or password are incorrect"
    LOGIN_SUCCESS = "Successfully logged in"
    REGISTRATION_SUCCESS = "User created successfully"
    UNAUTHORIZED = "You should be authorised"

class OrderMessages:
    CREATED_SUCCESS = "Order created successfully"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
    INVALID_INGREDIENTS = "One or more ingredient ids are invalid"
    INTERNAL_ERROR = "Internal Server Error"

class GeneralMessages:
    SUCCESS_TRUE = True
    SUCCESS_FALSE = False

class UserCreationMessages:
    SUCCESS_CREATION = "User created successfully"
    USER_EXISTS = "User already exists"
    MISSING_FIELDS = "Email, password and name are required fields"

class UserUpdateMessages:
    UNAUTHORIZED = "You should be authorised"
    UPDATE_SUCCESS = "User updated successfully"
    INVALID_CURRENT_PASSWORD = "Current password is incorrect"
    DUPLICATE_EMAIL = "User with this email already exists"
    INVALID_EMAIL_FORMAT = "Invalid email format"
    WEAK_PASSWORD = "Password must be at least 6 characters"
