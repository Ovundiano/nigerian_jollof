import os
import shutil
from PIL import Image
import cairosvg


class JollofImageOrganizer:
    def __init__(self):
        # Define base paths based on your actual structure
        self.project_root = os.getcwd()
        self.static_path = os.path.join('recipes', 'static', 'recipes')

        # Define all required directories
        self.directories = {
            'svg': os.path.join(self.static_path, 'img', 'svg'),
            'jpg': os.path.join(self.static_path, 'img', 'jpg'),
            'thumbnails': os.path.join(self.static_path, 'img', 'thumbnails'),
            'webp': os.path.join(self.static_path, 'img', 'webp'),
            'originals': os.path.join(self.static_path, 'img', 'originals')
        }

        # SVG content for each jollof type
        self.svg_content = {
            'smoky-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFF5E6"/>
    <circle cx="200" cy="150" r="100" fill="#FF4500"/>
    <path d="M150 150 Q200 100 250 150" stroke="#8B0000" fill="none" stroke-width="5"/>
    <path d="M160 170 Q200 220 240 170" fill="#8B0000"/>
    <circle cx="200" cy="150" r="80" fill="#FF6347" opacity="0.6"/>
</svg>''',
            'firewood-jollof': '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
    <rect width="400" height="300" fill="#FFE4B5"/>
    <path d="M100 200 L200 100 L300 200" fill="#A0522D"/>
    <circle cx="200" cy="150" r="90" fill="#FF4500"/>
    <path d="M150 140 L250 140" stroke="#8B0000" stroke-width="8"/>
    <path d="M170 160 L230 160" stroke="#8B0000" stroke-width="8"/>
</svg>''',
            # Add other SVG contents here
        }

    def setup_directories(self):
        """Create all necessary directories"""
        for dir_path in self.directories.values():
            os.makedirs(dir_path, exist_ok=True)
            print(f'Created/verified directory: {dir_path}')

    def create_svg_files(self):
        """Create SVG files in the svg directory"""
        for name, content in self.svg_content.items():
            file_path = os.path.join(self.directories['svg'], f'{name}.svg')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Created SVG file: {name}.svg')

    def backup_existing_images(self):
        """Backup existing JPG files to originals directory"""
        jpg_dir = os.path.join(self.static_path, 'img')
        for file in os.listdir(jpg_dir):
            if file.endswith('.jpg') and os.path.isfile(os.path.join(jpg_dir, file)):
                src = os.path.join(jpg_dir, file)
                dst = os.path.join(self.directories['originals'], file)
                shutil.copy2(src, dst)
                print(f'Backed up: {file}')

    def convert_images(self):
        """Convert SVG files to JPG and create thumbnails"""
        svg_dir = self.directories['svg']
        for svg_file in os.listdir(svg_dir):
            if svg_file.endswith('.svg'):
                base_name = os.path.splitext(svg_file)[0]

                # Convert to JPG
                svg_path = os.path.join(svg_dir, svg_file)
                jpg_path = os.path.join(self.directories['jpg'], f'{base_name}.jpg')
                webp_path = os.path.join(self.directories['webp'], f'{base_name}.webp')

                try:
                    # Convert SVG to PNG first
                    png_path = jpg_path.replace('.jpg', '.png')
                    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=800, output_height=600)

                    # Convert PNG to JPG and WebP
                    img = Image.open(png_path)
                    img.convert('RGB').save(jpg_path, 'JPEG', quality=95)
                    img.convert('RGB').save(webp_path, 'WEBP', quality=90)

                    # Create thumbnail
                    thumbnail_path = os.path.join(self.directories['thumbnails'], f'{base_name}.jpg')
                    img.thumbnail((300, 300))
                    img.save(thumbnail_path, 'JPEG', quality=85)

                    # Clean up PNG
                    os.remove(png_path)
                    print(f'Processed: {base_name}')
                except Exception as e:
                    print(f'Error processing {svg_file}: {str(e)}')


def main():
    organizer = JollofImageOrganizer()

    print("1. Setting up directory structure...")
    organizer.setup_directories()

    print("\n2. Backing up existing images...")
    organizer.backup_existing_images()

    print("\n3. Creating SVG files...")
    organizer.create_svg_files()

    print("\n4. Converting images to various formats...")
    organizer.convert_images()

    print("\nImage organization complete!")


if __name__ == "__main__":
    main()
