from PIL import Image

def binary_to_string(binary_data):
    # Convert binary data to a string
    message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        message += chr(int(byte, 2))
    return message

def string_to_binary(message):
    # Convert a string to binary data
    binary_data = ""
    for char in message:
        binary_data += format(ord(char), '08b')
    return binary_data

def hide_message(image_path, output_path, message):
    img = Image.open(image_path)
    width, height = img.size
    max_message_length = width * height * 3 // 8

    binary_data = string_to_binary(message)

    if len(binary_data) > max_message_length:
        raise ValueError("Message is too long to hide in the image.")

    binary_data += "0" * (max_message_length - len(binary_data))  # Pad with zeros

    index = 0
    for x in range(width):
        for y in range(height):
            pixel = list(img.getpixel((x, y)))

            for color_channel in range(3):
                if index < len(binary_data):
                    pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_data[index])
                    index += 1

            img.putpixel((x, y), tuple(pixel))

    img.save(output_path)

def extract_message(image_path):
    img = Image.open(image_path)
    width, height = img.size
    max_message_length = width * height * 3 // 8

    binary_data = ""

    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))

            for color_channel in range(3):
                binary_data += str(pixel[color_channel] & 1)

    binary_data = binary_data[:max_message_length]  # Trim any extra bits
    message = binary_to_string(binary_data)
    return message

def main():
    print("############### Welcome to Steganography Tool! ###############")
    
    while True:
        print("\nMenu:")
        print("1. Hide a message in an image\n")
        print("2. Extract a hidden message from an image\n")
        print("0. Exit\n")

        choice = input("Enter your choice (0, 1, or 2): ")

        if choice == "1":
            image_path = input("Enter the path of the input image: ")
            output_path = input("Enter the path of the steganography image: ")
            message = input("Enter the message to hide: ")
            try:
                hide_message(image_path, output_path, message)
                print("Message hidden successfully!")
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            image_path = input("Enter the path of the steganography image: ")
            try:
                extracted_message = extract_message(image_path)
                print("Extracted message:", extracted_message)
            except Exception as e:
                print("Error:", e)

        elif choice == "0":
            print("Exiting the Steganography Tool. Goodbye!")
            break

        else:
            print("\n###############         Invalid choice         ###############\n\n############### Please enter either 0, 1, or 2 ###############\n######################################################################################")

if _name_ == "_main_":
    main()
