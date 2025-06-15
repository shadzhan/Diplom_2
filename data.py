from faker import Faker
import time



fake = Faker()
timestamp = int(time.time())


NAME_UPDATE_CASES = [
    {"name": f"Updated Name 1_{timestamp}"},
    {"name": f"Updated Name 2_{timestamp+1}"},
    {"name": fake.name()},
]

EMAIL_UPDATE_CASES = [
    {"email": f"new_email1_{timestamp}@example.com"},
    {"email": f"new_email2_{timestamp+1}@example.com"},
    {"email": fake.email()},
]

PASSWORD_UPDATE_CASES = [
    {"password": "scarecrow12!"},
    {"password": "scarecrow22@"},
    {"password": fake.password(length=12)},
]

FULL_UPDATE_CASES = [
    {
        "email": "gatherwill4@gmail.com",
        "name": "Holly Crowley 2",
        "password": "HighwayToTheBar2!"
    },
    {
        "email": "gatherwill4@gmail.com",
        "name": "Holly Crowley 2",
        "password": "HighwayToTheBar2@"
    },
]

UNAUTHORIZED_UPDATE_CASES = [
    {"email": "creepy1@gmail.com"},
    {"name": "Saint John"},

]

WRONG_PASSWORD_CASES = [
    {"wrong_password": "Incorr3ctPa$$word1!"},
    {"wrong_password": "WronGP@ssw0rd2#"},
    {"wrong_password": fake.password(length=12)},
]