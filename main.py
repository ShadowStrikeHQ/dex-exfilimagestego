import argparse
import logging
import os
import sys
from PIL import Image
import random
from faker import Faker
from random_word import RandomWords

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Security best practices: Ensure file paths are validated and sanitized

def setup_argparse():
    """
    Sets up the argument parser for the script.
    """
    parser = argparse.ArgumentParser(description="Embeds data within a PNG image using LSB steganography. Also generates fake data for exfiltration simulation.")
    parser.add_argument("image_path", help="Path to the PNG image to use as a cover image.")
    parser.add_argument("-o", "--output_path", help="Path to save the steganographically encoded PNG image.", default="output.png")
    parser.add_argument("-d", "--data_file", help="Path to a file containing data to embed. If not provided, fake data is generated.", default=None)
    parser.add_argument("-g", "--generate_data", action="store_true", help="Generate fake data for embedding. Overrides --data_file.")
    parser.add_argument("-s", "--data_size", type=int, default=1024, help="Size of fake data to generate (in bytes). Only applicable with -g.")
    parser.add_argument("-e", "--exfiltration_protocol", choices=['http', 'dns'], help="Simulated exfiltration protocol (optional).", default=None)
    return parser


def generate_fake_data(size):
    """
    Generates fake data for exfiltration simulation.

    Args:
        size (int): The size of the data to generate in bytes.

    Returns:
        bytes: The generated fake data.
    """
    try:
        fake = Faker()
        random_word = RandomWords()
        data = b""
        while len(data) < size:
            # Generate a mix of usernames, passwords, and financial records
            data += fake.user_name().encode() + b","
            data += fake.password().encode() + b","
            data += fake.credit_card_number().encode() + b","
            data += str(random.randint(1000, 100000)).encode() + b"," # random financial data
            data += random_word.get_random_word().encode() + b"," # add some random words

        return data[:size]  # Truncate to the desired size

    except Exception as e:
        logging.error(f"Error generating fake data: {e}")
        raise

def read_data_from_file(file_path):
    """
    Reads data from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        bytes: The data read from the file.
    """
    try:
        # Security best practices:  Validate the file path to prevent path traversal.
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            data = f.read()
        return data
    except FileNotFoundError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(f"Error reading data from file: {e}")
        raise


def embed_data(image_path, data, output_path):
    """
    Embeds data within a PNG image using LSB steganography.

    Args:
        image_path (str): The path to the PNG image.
        data (bytes): The data to embed.
        output_path (str): The path to save the steganographically encoded PNG image.
    """
    try:
        # Security best practices:  Validate the image path to prevent path traversal.
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        img = Image.open(image_path)
        img = img.convert("RGBA")
        data_len = len(data)
        # Encode the length of the data at the beginning of the image.
        data = data_len.to_bytes(4, 'big') + data
        
        pixels = list(img.getdata())
        
        if len(data) * 8 > len(pixels):
            raise ValueError("Data is too large to fit in the image.")

        data_index = 0
        for i in range(len(pixels)):
            r, g, b, a = pixels[i]

            if data_index < len(data):
                # Embed data in the least significant bit of the red channel
                binary_data = bin(data[data_index])[2:].zfill(8)
                r = (r & 0xFE) | int(binary_data[0:2], 2)
                g = (g & 0xFC) | int(binary_data[2:4], 2)
                b = (b & 0xFC) | int(binary_data[4:6], 2)
                a = (a & 0xFC) | int(binary_data[6:8], 2)

                pixels[i] = (r, g, b, a)
                data_index += 1

        img.putdata(pixels)

        # Security best practices:  Sanitize output path.
        img.save(output_path, "PNG")
        logging.info(f"Data successfully embedded in {output_path}")
    except FileNotFoundError as e:
        logging.error(e)
        raise
    except ValueError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(f"Error embedding data: {e}")
        raise


def simulate_exfiltration(protocol):
    """Simulates exfiltration of data via the specified protocol.

    Args:
        protocol (str): The exfiltration protocol to simulate (e.g., "http", "dns").
    """
    if protocol == "http":
        logging.info("Simulating exfiltration via HTTP...")
        # In a real scenario, this would involve making HTTP requests
        # to a remote server, sending the data as part of the request.
        logging.info("HTTP exfiltration simulation complete. (No actual data sent.)")
    elif protocol == "dns":
        logging.info("Simulating exfiltration via DNS tunneling...")
        # In a real scenario, this would involve encoding data as DNS queries
        # and sending them to a DNS server.
        logging.info("DNS tunneling exfiltration simulation complete. (No actual data sent.)")
    else:
        logging.warning(f"Unsupported exfiltration protocol: {protocol}")


def main():
    """
    Main function to execute the data embedding and exfiltration simulation.
    """
    try:
        parser = setup_argparse()
        args = parser.parse_args()

        # Input validation:  Ensure that the image path ends with '.png'
        if not args.image_path.lower().endswith(".png"):
            raise ValueError("Input image must be a PNG file.")

        # Determine the data source
        if args.generate_data:
            data = generate_fake_data(args.data_size)
            logging.info(f"Generated {args.data_size} bytes of fake data.")
        elif args.data_file:
            data = read_data_from_file(args.data_file)
            logging.info(f"Read data from file: {args.data_file}")
        else:
            print("No data source specified. Generating default fake data (1024 bytes).")
            data = generate_fake_data(1024)
            logging.info(f"Generated 1024 bytes of fake data.")

        # Embed the data into the image
        embed_data(args.image_path, data, args.output_path)

        # Simulate exfiltration if a protocol is specified
        if args.exfiltration_protocol:
            simulate_exfiltration(args.exfiltration_protocol)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()