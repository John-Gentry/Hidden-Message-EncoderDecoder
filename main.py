import numpy as np
from PIL import Image
source_image = "steg.png"

def extract_message(image_path):
  picture = Image.open(image_path, 'r')
  pixel_array = np.array(list(picture.getdata()))
  print("Picture mode is: "+str(picture.mode))
  if picture.mode == 'RGB':
      channel_count = 3 # 3 channels
  elif picture.mode == 'RGBA':
      channel_count = 4 # 4 channels
  pixel_total = pixel_array.size//channel_count #count number of pixels

  secret_bits = ""
  for pixel in range(pixel_total):
      for color in range(0, 3): #default to 3 channels
          secret_bits += (bin(pixel_array[pixel][color])[2:][-1])
  
  secret_bits_chunks = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]
  print("Number of bytes to parse: " + str(len(secret_bits_chunks)))
  decoded_message = ""
  for bit_chunk in range(len(secret_bits_chunks)):
      if decoded_message[-5:] == "$g6o0": #if key was found in this position it would generate a blank message
          break
      else:
          decoded_message += chr(int(secret_bits_chunks[bit_chunk], 2))
  if "$g6o0" in decoded_message:
      print("Decoded:", decoded_message[:-5])
  else:
      print("No Hidden Message Found")

def hide_message(original_image, secret_message, target_image):

  source_picture = Image.open(original_image, 'r')
  pic_width, pic_height = source_picture.size # saves these values for reforming the image
  pixel_array = np.array(list(source_picture.getdata())) #generates a numpy array of the pixels

  if source_picture.mode == 'RGB':
      channel_count = 3 # 3 channels
  elif source_picture.mode == 'RGBA':
      channel_count = 4 # 4 channels
  pixel_total = pixel_array.size//channel_count #count number of pixels

  secret_message += "$g6o0" #add key to end of message
  binary_message = ''.join([format(ord(char), "08b") for char in secret_message])
  required_pixels = len(binary_message) #counts your message length

  if required_pixels > pixel_total: #the steg is limited to the number of pixels the image has
      print("ERROR: Need larger file size")

  else:
      bit_index = 0
      for pixel in range(pixel_total):
          for color in range(0, 3): #default to 3 channel system
              if bit_index < required_pixels: #adds a LSB to the end of each individual pixel
                  pixel_array[pixel][color] = int(bin(pixel_array[pixel][color])[2:9] + binary_message[bit_index], 2)
                  bit_index += 1

      pixel_array = pixel_array.reshape(pic_height, pic_width, channel_count) #with binary of the pixels adjusted, reshape the image using the same parameters
      encoded_image = Image.fromarray(pixel_array.astype('uint8'), source_picture.mode) #generates image from pixel_array, using 8 bit unsigned (non negative numbers), with the channels required for the image
      encoded_image.save(target_image)
      print("Image Encoded Successfully")

hide_message("cat.jpeg", "This is a steg", "/home/runner/Steg-Detection/steg.png")
extract_message(source_image)
