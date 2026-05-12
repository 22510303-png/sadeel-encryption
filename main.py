import cv2
import numpy as np
import os

def text_to_binary(text):
    return ''.join([format(ord(i), "08b") for i in text])

def encode_image(img_path, secret_data, output_path):
    img = cv2.imread(img_path)
    if img is None: return False
    
    secret_data += "#####"
    binary_data = text_to_binary(secret_data)
    
    flat_img = img.flatten()
    if len(binary_data) > len(flat_img): return False
    
    for i in range(len(binary_data)):
        flat_img[i] = (flat_img[i] & 254) | int(binary_data[i])
        
    res_img = flat_img.reshape(img.shape)
    cv2.imwrite(output_path, res_img)
    return True

def decode_image(img_path):
    img = cv2.imread(img_path)
    if img is None: return "Error"
    
    flat_img = img.flatten()
    binary_data = "".join([str(pixel & 1) for pixel in flat_img])
    
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    
    decoded_text = ""
    for byte in all_bytes:
        decoded_text += chr(int(byte, 2))
        if decoded_text.endswith("#####"):
            break
            
    return decoded_text[:-5]

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    
    input_img = ""
    for f in os.listdir(path):
        if f.lower().startswith("lena") and f.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_img = os.path.join(path, f)
            break
            
    output_img = os.path.join(path, "lena_final.png")
    message = "Success for Dr"
    
    if input_img:
        if encode_image(input_img, message, output_img):
            print("DONE: Lena image encoded successfully!")
            extracted_msg = decode_image(output_img)
            print(f"Extracted Message: {extracted_msg}")