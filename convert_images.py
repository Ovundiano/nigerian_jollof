import os
import shutil
from PIL import Image
import cairosvg
import logging
from pathlib import Path
from django.conf import settings


class JollofImageOrganizer:
    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Define base paths
        self.project_root = os.getcwd()
        self.static_path = os.path.join('recipes', 'static', 'recipes')

        # Ensure static path is included in Django's STATICFILES_DIRS
        self.static_url = '/static/recipes/img/'

        # Define directories
        self.directories = {
            'svg': os.path.join(self.static_path, 'img', 'svg'),
            'jpg': os.path.join(self.static_path, 'img', 'jpg'),
            'thumbnails': os.path.join(self.static_path, 'img', 'thumbnails'),
            'webp': os.path.join(self.static_path, 'img', 'webp'),
            'originals': os.path.join(self.static_path, 'img', 'originals')
        }

        # SVG content for each jollof type with enhanced visuals
        self.svg_content = {
            'smoky-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFF5E6"/>
    <circle cx="200" cy="150" r="100" fill="#FF4500"/>
    <path d="M150 150 Q200 100 250 150" stroke="#8B0000" fill="none" stroke-width="5"/>
    <path d="M160 170 Q200 220 240 170" fill="#8B0000"/>
    <circle cx="200" cy="150" r="80" fill="#FF6347" opacity="0.6"/>
    <path d="M180 120 Q200 100 220 120" stroke="#4A0404" fill="none" stroke-width="3"/>
</svg>''',
            'firewood-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFE4B5"/>
    <path d="M100 200 L200 100 L300 200" fill="#8B4513"/>
    <circle cx="200" cy="150" r="90" fill="#FF4500"/>
    <path d="M150 140 L250 140" stroke="#8B0000" stroke-width="8"/>
    <path d="M170 160 L230 160" stroke="#8B0000" stroke-width="8"/>
    <path d="M160 180 C180 170 220 170 240 180" stroke="#FFD700" stroke-width="3"/>
</svg>''',
            'coconut-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFF8DC"/>
    <circle cx="200" cy="150" r="95" fill="#FF6347"/>
    <circle cx="200" cy="150" r="85" fill="#FF4500"/>
    <path d="M150 130 Q200 180 250 130" fill="#FFFFFF" opacity="0.3"/>
    <circle cx="170" cy="140" r="15" fill="#FFFFFF" opacity="0.5"/>
    <circle cx="230" cy="140" r="15" fill="#FFFFFF" opacity="0.5"/>
</svg>''',
            'party-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFE4E1"/>
    <circle cx="200" cy="150" r="100" fill="#FF4500"/>
    <path d="M150 150 L250 150" stroke="#FFD700" stroke-width="5"/>
    <path d="M180 120 L220 120" stroke="#FFD700" stroke-width="5"/>
    <path d="M180 180 L220 180" stroke="#FFD700" stroke-width="5"/>
    <circle cx="200" cy="150" r="80" fill="#FF6347" opacity="0.4"/>
</svg>''',
            'quick-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFF0F5"/>
    <circle cx="200" cy="150" r="90" fill="#FF4500"/>
    <path d="M160 150 L240 150" stroke="#8B0000" stroke-width="6"/>
    <circle cx="200" cy="150" r="70" fill="#FF6347" opacity="0.5"/>
    <path d="M180 130 Q200 110 220 130" stroke="#4A0404" fill="none" stroke-width="3"/>
</svg>''',
            'native-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFF5EE"/>
    <circle cx="200" cy="150" r="95" fill="#FF4500"/>
    <path d="M150 140 Q200 90 250 140" stroke="#8B0000" fill="none" stroke-width="4"/>
    <path d="M160 160 Q200 210 240 160" fill="#8B0000"/>
    <circle cx="200" cy="150" r="75" fill="#FF6347" opacity="0.5"/>
    <path d="M170 130 Q200 150 230 130" stroke="#FFD700" stroke-width="3" fill="none"/>
</svg>'''
        }

    def setup_directories(self):
        """Create all necessary directories with error handling"""
        for dir_name, dir_path in self.directories.items():
            try:
                os.makedirs(dir_path, exist_ok=True)
                self.logger.info(f'Created/verified directory: {dir_path}')
            except Exception as e:
                self.logger.error(f'Error creating directory {dir_name}: {str(e)}')
                raise

    def create_svg_files(self):
        """Create SVG files with error handling"""
        for name, content in self.svg_content.items():
            file_path = os.path.join(self.directories['svg'], f'{name}.svg')
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.logger.info(f'Created SVG file: {name}.svg')
            except Exception as e:
                self.logger.error(f'Error creating SVG file {name}: {str(e)}')
                raise

    def backup_existing_images(self):
        """Backup existing images with error handling"""
        jpg_dir = os.path.join(self.static_path, 'img')
        try:
            if not os.path.exists(self.directories['originals']):
                os.makedirs(self.directories['originals'])

            for file in os.listdir(jpg_dir):
                if file.endswith('.jpg') and os.path.isfile(os.path.join(jpg_dir, file)):
                    src = os.path.join(jpg_dir, file)
                    dst = os.path.join(self.directories['originals'], file)
                    shutil.copy2(src, dst)
                    self.logger.info(f'Backed up: {file}')
        except Exception as e:
            self.logger.error(f'Error during backup: {str(e)}')
            raise

    def convert_images(self):
        """Convert SVG files to multiple formats with enhanced error handling"""
        svg_dir = self.directories['svg']
        for svg_file in os.listdir(svg_dir):
            if svg_file.endswith('.svg'):
                base_name = os.path.splitext(svg_file)[0]
                svg_path = os.path.join(svg_dir, svg_file)

                try:
                    # Convert to PNG first (temporary)
                    png_path = os.path.join(self.directories['jpg'], f'{base_name}_temp.png')
                    cairosvg.svg2png(
                        url=svg_path,
                        write_to=png_path,
                        output_width=800,
                        output_height=600,
                        scale=2.0  # Increase resolution
                    )

                    # Process the image with Pillow
                    with Image.open(png_path) as img:
                        # Save as JPG
                        jpg_path = os.path.join(self.directories['jpg'], f'{base_name}.jpg')
                        img.convert('RGB').save(jpg_path, 'JPEG', quality=95, optimize=True)

                        # Save as WebP
                        webp_path = os.path.join(self.directories['webp'], f'{base_name}.webp')
                        img.convert('RGB').save(webp_path, 'WEBP', quality=90, method=6)

                        # Create thumbnail
                        thumbnail = img.copy()
                        thumbnail.thumbnail((300, 300), Image.Resampling.LANCZOS)
                        thumbnail_path = os.path.join(self.directories['thumbnails'], f'{base_name}.jpg')
                        thumbnail.save(thumbnail_path, 'JPEG', quality=85, optimize=True)

                    # Clean up temporary PNG
                    os.remove(png_path)
                    self.logger.info(f'Successfully processed: {base_name}')

                except Exception as e:
                    self.logger.error(f'Error processing {svg_file}: {str(e)}')
                    continue

    def verify_images(self):
        """Verify all images were created correctly"""
        expected_formats = ['jpg', 'webp', 'thumbnails']
        all_good = True

        for svg_file in os.listdir(self.directories['svg']):
            base_name = os.path.splitext(svg_file)[0]
            for format_dir in expected_formats:
                expected_path = os.path.join(self.directories[format_dir],
                                           f'{base_name}.{"jpg" if format_dir != "webp" else "webp"}')
                if not os.path.exists(expected_path):
                    self.logger.error(f'Missing {format_dir} file for {base_name}')
                    all_good = False
                else:
                    try:
                        # Verify image can be opened
                        Image.open(expected_path).verify()
                    except Exception as e:
                        self.logger.error(f'Corrupted {format_dir} file for {base_name}: {str(e)}')
                        all_good = False

        return all_good


def main():
    try:
        organizer = JollofImageOrganizer()

        print("1. Setting up directory structure...")
        organizer.setup_directories()

        print("\n2. Backing up existing images...")
        organizer.backup_existing_images()

        print("\n3. Creating SVG files...")
        organizer.create_svg_files()

        print("\n4. Converting images to various formats...")
        organizer.convert_images()

        print("\n5. Verifying converted images...")
        if organizer.verify_images():
            print("All images converted successfully!")
        else:
            print("Some images may have issues. Check the logs for details.")

    except Exception as e:
        print(f"\nError during image organization: {str(e)}")
        raise


if __name__ == "__main__":
    main()
