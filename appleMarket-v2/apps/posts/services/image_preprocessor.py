import cv2
import numpy as np

class ImagePreprocessor:
    @staticmethod
    def preprocess(image_file):
        
        file_bytes = np.fromstring(image_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        scale_percent = 300
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        binary_img = cv2.adaptiveThreshold(
            gray, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            21, 
            5
        )

        kernel = np.ones((2, 2), np.uint8)
        thickened_img = cv2.erode(binary_img, kernel, iterations=1)

        inverted_img = cv2.bitwise_not(thickened_img)
        
        return [thickened_img, inverted_img]