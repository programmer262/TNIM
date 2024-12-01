import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QLineEdit, QHBoxLayout, QWidget, QMessageBox, QComboBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PIL import Image as im
import numpy as np
import skimage as ski
from skimage import filters
from skimage.util import random_noise
from skimage.morphology import square
from skimage.filters import gaussian, rank

def filtre_moyenneur(image_path, dimensions):
    img = im.open(image_path)
    array = np.asarray(img)
    footprint = square(dimensions)
    if img.mode == "RGB":
        r = array[:,:,0]
        g = array[:,:,1]
        b = array[:,:,2]
        r_array = rank.mean(r, footprint=footprint)
        g_array = rank.mean(g, footprint=footprint)
        b_array = rank.mean(b, footprint=footprint)
        normal_result = np.stack((r_array, g_array, b_array), axis=2)
    else:
        normal_result = rank.mean(array, footprint=footprint)

    image = im.fromarray(normal_result.astype("uint8"))
    image.save('filtre_moyenneur.png')
    return image
def contraste(path):
    image = im.open(path)
    array2 = np.asarray(image)
    array = array2.copy()
    if image.mode=='L' or image.mode=='P':
        max_gris=np.max(array)
        min_gris = np.min(array)
        Cr_gris = (max_gris - min_gris) / (max_gris + min_gris)
        contrastez = (array-min_gris)*Cr_gris
        image_output = im.fromarray(contrastez.astype("uint8"))
        image_output.save('image_output_contrast.png')
    else:
        red = array[:,:,0]
        blue = array[:,:,2]
        green = array[:,:,1]
        max_red = np.max(red)
        min_red = np.min(red)
        max_green = np.max(green)
        min_green = np.min(green)
        max_blue = np.max(blue)
        min_blue = np.min(blue)
        Cr_red = (max_red - min_red) / (max_red + min_red)
        Cr_blue = (max_blue - min_blue) / (max_blue + min_blue)
        Cr_green = (max_green - min_green) / (max_green + min_green)
        contraste_rouge = (red-min_red)*Cr_red
        contraste_vert = (green-min_green)*Cr_green
        contraste_blue = (blue-min_blue)*Cr_blue
        constrastez = np.stack((contraste_rouge, contraste_vert, contraste_blue), axis=2)
    
        image_output = im.fromarray(constrastez.astype("uint8"))
        image_output.save('image_output_contrast.png')
    return image_output
def filtre_mediane(image_path, dimensions):
    img = im.open(image_path)
    array = np.asarray(img)
    footprint = square(dimensions)
    if img.mode == "RGB":
        r = array[:,:,0]
        g = array[:,:,1]
        b = array[:,:,2]
        r_array = rank.median(r, footprint=footprint)
        g_array = rank.median(g, footprint=footprint)
        b_array = rank.median(b, footprint=footprint)
        normal_result = np.stack((r_array, g_array, b_array), axis=2)
    else:
        normal_result = rank.median(array, footprint=footprint)

    image = im.fromarray(normal_result.astype("uint8"))
    image.save('filtre_mediane.png')
    return image

def bruité_image(mod, image_path):
    image = im.open(image_path)
    image_array = np.asarray(image)
    if image.mode == "RGB":
        red = image_array[:, :, 0]
        green = image_array[:, :, 1]
        blue = image_array[:, :, 2]
        
        noise_modes = {
            "gaussian": "gaussian",
            "multiplicatif": "speckle",
            "impulsif": "s&p",
            "sel": "salt",
            "poivre": "pepper",
            "poisson": "poisson"
        }
        
        if mod not in noise_modes:
            raise ValueError("Invalid noise type")
        
        random_array_red = random_noise(red, mode=noise_modes[mod])
        random_array_green = random_noise(green, mode=noise_modes[mod])
        random_array_blue = random_noise(blue, mode=noise_modes[mod])
        
        noisy_array = np.stack((random_array_red, random_array_green, random_array_blue), axis=2)
        noisy_image_data = np.clip(noisy_array * 255, 0, 255).astype("uint8")
        
        noisy_image = im.fromarray(noisy_image_data)
        noisy_image.save("noisy_image.png")
        return noisy_image
    else:
        raise ValueError("Unsupported image mode. Only RGB images are supported.")
def dynamique(path):
    image = im.open(path)
    width,height = image.size
    array = np.asarray(image)
    if image.mode=="RGB":
        red = array[:,:,0]
        blue = array[:,:,2]
        green = array[:,:,1]
        max_red = np.max(red)
        min_red = np.min(red)
        I2_red= (red - min_red) * (255/max_red-min_red)
        max_green = np.max(green)
        min_green = np.min(green)
        I2_green= (green-min_green)*(255/max_green-min_green)
        max_blue = np.max(blue)
        min_blue = np.min(blue)
        I2_blue=(blue-min_blue)*(255/max_blue-min_blue)
        I2_blue=(np.clip(I2_blue,0,255)).astype("uint8")
        I2_red=(np.clip(I2_red,0,255)).astype("uint8")
        I2_green=(np.clip(I2_green,0,255)).astype("uint8")
        red_image =im.fromarray((I2_red*255).astype("uint8"))
        green_image =im.fromarray((I2_green*255).astype("uint8"))
        blue_image =im.fromarray((I2_blue*255).astype("uint8"))
        rgb_array = np.stack((I2_red, I2_green, I2_blue), axis=2)
        image_output = im.fromarray(rgb_array)
    else :
        Nmax = np.max(array)
        Nmin = np.min(array)
        I2= (array-Nmin)*(255/(Nmax-Nmin))
        I2=(np.clip(I2,0,255)).astype("uint8")
        image_output =im.fromarray(I2)
    image_output.save('image_output_dynamique.jpeg')
    return image_output
def filtre_gaussian(image_path, sigma):
    img = im.open(image_path)
    array = np.asarray(img)
    if img.mode=="RGB":
        r = array[:,:,0]
        g = array[:,:,1]
        b = array[:,:,2]
        r_array = r * gaussian(r, sigma=sigma)
        g_array = g * gaussian(g, sigma=sigma)
        b_array = b * gaussian(b, sigma=sigma)
        r_array = np.clip(r_array, 0, 255)
        g_array = np.clip(g_array, 0, 255)
        b_array = np.clip(b_array, 0, 255)

        normal_result = np.stack((r_array, g_array, b_array), axis=2)
    else:
        gaussien = gaussian(array, sigma = sigma)
        normal_result = array * gaussien
    image = im.fromarray(normal_result.astype("uint8"))
    image.save('filtre_gaussian.png')
    return image

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Processing GUI")
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Input layouts... (same as original code)
        self.footprint_input_layout = QHBoxLayout()
        self.footprint_label = QLabel("Footprint Size:")
        self.footprint_input = QLineEdit()
        self.footprint_input.setPlaceholderText("Enter size (e.g., 3)")
        self.footprint_input_layout.addWidget(self.footprint_label)
        self.footprint_input_layout.addWidget(self.footprint_input)
        self.layout.addLayout(self.footprint_input_layout)

        self.sigma_input_layout = QHBoxLayout()
        self.sigma_label = QLabel("Sigma:")
        self.sigma_input = QLineEdit()
        self.sigma_input.setPlaceholderText("Enter sigma value (e.g., 1.0)")
        self.sigma_input_layout.addWidget(self.sigma_label)
        self.sigma_input_layout.addWidget(self.sigma_input)
        self.layout.addLayout(self.sigma_input_layout)

        self.noise_input_layout = QHBoxLayout()
        self.noise_label = QLabel("Noise Type:")
        self.noise_combo = QComboBox()
        self.noise_combo.addItems(["gaussian", "multiplicatif", "impulsif", "sel", "poivre", "poisson"])
        self.noise_input_layout.addWidget(self.noise_label)
        self.noise_input_layout.addWidget(self.noise_combo)
        self.layout.addLayout(self.noise_input_layout)

        # Buttons
        self.open_button = QPushButton("Open Image")
        self.noise_button = QPushButton("Add Noise")
        self.median_button = QPushButton("Apply Median Filter")
        self.mean_button = QPushButton("Apply Mean Filter")
        self.gaussian_button = QPushButton("Apply Gaussian Filter")
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.noise_button)
        self.layout.addWidget(self.median_button)
        self.layout.addWidget(self.mean_button)
        self.layout.addWidget(self.gaussian_button)

        # Image Labels
        self.original_label = QLabel("Original Image")
        self.processed_label = QLabel("Processed Image")
        self.layout.addWidget(self.original_label)
        self.layout.addWidget(self.processed_label)

        # Connections
        self.open_button.clicked.connect(self.open_image)
        self.noise_button.clicked.connect(self.apply_noise)
        self.median_button.clicked.connect(lambda: self.apply_filter("median"))
        self.mean_button.clicked.connect(lambda: self.apply_filter("mean"))
        self.gaussian_button.clicked.connect(self.apply_gaussian_filter)
        self.dynamic_range_button = QPushButton("Dynamic Range Adjustment")
        self.contrast_enhancement_button = QPushButton("Contrast Enhancement")
        
        # Add new buttons to layout
        self.layout.addWidget(self.dynamic_range_button)
        self.layout.addWidget(self.contrast_enhancement_button)

        # Connect new buttons to methods
        self.dynamic_range_button.clicked.connect(self.apply_dynamic_range)
        self.contrast_enhancement_button.clicked.connect(self.apply_contrast_enhancement)

        # Attributes
        self.image_path = None

    def open_image(self):
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.original_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def apply_noise(self):
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "No image selected!")
            return

        noise_type = self.noise_combo.currentText()
        try:
            noisy_image = bruité_image(noise_type, self.image_path)
            noisy_image_path = "noisy_image.png"
            noisy_image.save(noisy_image_path)
            self.display_processed_image(noisy_image_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply noise: {e}")

    def apply_filter(self, filter_type):
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "No image selected!")
            return

        try:
            footprint_size = int(self.footprint_input.text())
            if footprint_size <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid positive integer for footprint size.")
            return

        try:
            if filter_type == "median":
                processed_image = filtre_mediane(self.image_path, footprint_size)
            elif filter_type == "mean":
                processed_image = filtre_moyenneur(self.image_path, footprint_size)
            
            processed_image_path = os.path.join(os.getcwd(), f"processed_image_filter_{filter_type}.png")
            processed_image.save(processed_image_path)
            self.display_processed_image(processed_image_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply {filter_type} filter: {e}")

    def apply_gaussian_filter(self):
        if not self.image_path:
            QMessageBox.warning(self, "Warning", "No image selected!")
            return

        try:
            sigma = float(self.sigma_input.text())
            if sigma <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid positive value for sigma.")
            return

        try:
            processed_image = filtre_gaussian(self.image_path, sigma)
            processed_image_path = os.path.join(os.getcwd(), "processed_image_gaussian.png")
            processed_image.save(processed_image_path)
            self.display_processed_image(processed_image_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply Gaussian filter: {e}")
    def apply_dynamic_range(self):
        try:
            # Add a method to get file path (you'll need to implement this)
            path = self.get_image_path()
            if not path:
                return
            
            processed_image = dynamique(path)
            processed_image_path = os.path.join(os.getcwd(), "dynamic_range_image.png")
            processed_image.save(processed_image_path)
            self.display_processed_image(processed_image_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Dynamic range adjustment failed: {e}")


    def apply_contrast_enhancement(self):
        try:
            path = self.get_image_path()
            if not path:
                return
            
            processed_image = contraste(path)
            
            # Save images
            processed_path = os.path.join(os.getcwd(), "contrast_enhanced_image.png")
            
            processed_image.save(processed_path)
            
            self.display_processed_image(processed_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Contrast enhancement failed: {e}")


    def get_image_path(self):
        # Similar to open_image method, but returns path
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        return image_path

    def display_processed_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.processed_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

# Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec())