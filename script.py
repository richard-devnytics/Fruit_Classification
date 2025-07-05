import cv2

class camera():
    def capture_image(self):
        # Open the default camera
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)

        # Capture a single frame
        result, image = cam.read()

        if result:
            # Convert to RGB format if needed (OpenCV uses BGR format by default)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            img_path = "captured_image.png"
            self.img_path = img_path

            # Save the image
            cv2.imwrite(img_path, image_rgb)

            # Update image source in UI

            # Release the camera
            cam.release()
        else:
            print("No image detected. Please try again.")
            cam.release()

if __name__ == '__main__':
    cam = camera()
    cam.capture_image()
