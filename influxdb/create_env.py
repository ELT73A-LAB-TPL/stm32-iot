import os
# import secrets # No longer needed
# import string # No longer needed
from faker import Faker # Import Faker

def create_influxdb_env_file():
    """
    Creates a .env file with randomly generated InfluxDB configuration variables using Faker.
    """
    env_file_path = '.env'

    # Initialize Faker
    fake = Faker()

    print("This script will create a .env file for your InfluxDB Docker Compose setup.")
    print("It will generate random values for username, password, and token using Faker.")
    print("Make sure you have 'faker' installed (pip install faker).")
    print("-" * 60)

    # Generate random values using Faker
    username = fake.user_name() # Generates a realistic-looking username
    password = fake.password(length=12) # Generates a strong password of 20 characters
    token = fake.pystr(min_chars=40, max_chars=40) # Generates a random string of 40 characters for the token

    # Prepare content for the .env file
    env_content = f"""\
# Environment variables for InfluxDB Docker Compose
# These variables are used by the influxdb2 service in docker-compose.yml
# Randomly generated values for enhanced security, generated using Faker.

INFLUXDB_USERNAME={username}
INFLUXDB_PASSWORD={password}
INFLUXDB_TOKEN={token}
"""

    # Write content to the .env file
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"\nSuccessfully created {env_file_path} with the following content:")
        print("-" * 60)
        print(env_content)
        print("-" * 60)
        print(f"Make sure {env_file_path} is in the same directory as your docker-compose.yml file.")
        print("Remember to keep these values secure, especially the token!")
    except IOError as e:
        print(f"Error creating {env_file_path}: {e}")

if __name__ == "__main__":
    create_influxdb_env_file()
