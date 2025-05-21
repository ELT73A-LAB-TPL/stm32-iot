import os
import secrets
import string

def generate_random_string(length=16):
    """Generate a random string of specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

def create_influxdb_env_file():
    """
    Creates a .env file with randomly generated InfluxDB configuration variables.
    """
    env_file_path = '.env'

    print("This script will create a .env file for your InfluxDB Docker Compose setup.")
    print("It will generate random values for username, password, and token.")
    print("-" * 60)

    # Generate random values
    username = generate_random_string(10) # Shorter for username
    password = generate_random_string(20)
    token = generate_random_string(40) # Longer for token for better security

    # Prepare content for the .env file
    env_content = f"""\
# Environment variables for InfluxDB Docker Compose
# These variables are used by the influxdb2 service in docker-compose.yml
# Randomly generated values for enhanced security.

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
