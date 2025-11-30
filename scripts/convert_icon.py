from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path):
    try:
        img = Image.open(png_path)
        # Create sizes for the icon
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, format='ICO', sizes=icon_sizes)
        print(f"Successfully converted {png_path} to {ico_path}")
    except Exception as e:
        print(f"Error converting icon: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    assets_dir = os.path.join(root_dir, 'assets')
    
    input_png = os.path.join(assets_dir, "dahora_icon.png")
    output_ico = os.path.join(root_dir, "icon.ico")
    
    if os.path.exists(input_png):
        convert_png_to_ico(input_png, output_ico)
    else:
        print(f"Input file not found: {input_png}")
