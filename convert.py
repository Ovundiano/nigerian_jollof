import os
import logging
from pathlib import Path
from PIL import Image, ImageDraw


class JollofImageOrganizer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Use absolute paths based on Django project structure
        self.project_root = Path(__file__).resolve().parent
        self.static_path = os.path.join(
            self.project_root, "recipes", "static", "recipes"
        )

        # Define directories
        self.directories = {
            "jpg": os.path.join(self.static_path, "img"),
            "thumbnails": os.path.join(self.static_path, "img", "thumbnails"),
            "webp": os.path.join(self.static_path, "img", "webp"),
        }

        # Define colors for different jollof types
        self.jollof_types = {
            "smoky-jollof": "#FF4500",
            "firewood-jollof": "#8B4513",
            "coconut-jollof": "#FF6347",
            "party-jollof": "#FF6B6B",
            "quick-jollof": "#FF7F50",
            "native-jollof": "#CD5C5C",
        }

    def setup_directories(self):
        """Create all necessary directories"""
        for dir_path in self.directories.values():
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")

    def create_jollof_image(self, name, color):
        """Create a simple image for each jollof type"""
        # Create base image
        img = Image.new("RGB", (800, 600), "white")
        draw = ImageDraw.Draw(img)

        # Draw a colored rectangle to represent the jollof
        draw.rectangle([100, 100, 700, 500], fill=color)

        # Save as JPG
        jpg_path = os.path.join(self.directories["jpg"], f"{name}.jpg")
        img.save(jpg_path, "JPEG", quality=95)
        print(f"Created JPG: {jpg_path}")

        # Save as WebP
        webp_path = os.path.join(self.directories["webp"], f"{name}.webp")
        img.save(webp_path, "WEBP", quality=90)
        print(f"Created WebP: {webp_path}")

        # Create and save thumbnail
        thumbnail = img.copy()
        thumbnail.thumbnail((300, 300))
        thumbnail_path = os.path.join(self.directories["thumbnails"], f"{name}.jpg")
        thumbnail.save(thumbnail_path, "JPEG", quality=85)
        print(f"Created thumbnail: {thumbnail_path}")

    def create_all_images(self):
        """Create images for all jollof types"""
        for name, color in self.jollof_types.items():
            try:
                self.create_jollof_image(name, color)
                print(f"Successfully created all images for {name}")
            except Exception as e:
                print(f"Error creating images for {name}: {str(e)}")

    def verify_images(self):
        """Verify all images were created correctly"""
        all_good = True
        for name in self.jollof_types.keys():
            for format_dir in self.directories.keys():
                ext = ".webp" if format_dir == "webp" else ".jpg"
                path = os.path.join(self.directories[format_dir], f"{name}{ext}")
                if not os.path.exists(path):
                    print(f"Missing {format_dir} file for {name}")
                    all_good = False
                else:
                    try:
                        Image.open(path).verify()
                    except Exception as e:
                        print(f"Corrupted {format_dir} file for {name}: {str(e)}")
                        all_good = False
        return all_good


def main():
    try:
        print("Starting image creation process...")
        organizer = JollofImageOrganizer()

        print("\n1. Setting up directories...")
        organizer.setup_directories()

        print("\n2. Creating images...")
        organizer.create_all_images()

        print("\n3. Verifying images...")
        if organizer.verify_images():
            print("All images created successfully!")
        else:
            print("Some images may have issues. Check the logs for details.")

    except Exception as e:
        print(f"\nError during image creation: {str(e)}")
        raise


if __name__ == "__main__":
    main()
