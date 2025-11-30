from PIL import Image, ImageDraw

def create_icons():
    size = (256, 256)
    
    def draw_icon(is_paused=False):
        # Create transparent image
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        if is_paused:
            primary = (80, 80, 80, 255)    # Dark Gray
            secondary = (180, 180, 180, 255) # Light Gray
            bg_fill = (200, 200, 200, 255) # Lighter Gray for calendar body
        else:
            primary = (0, 120, 215, 255)   # Windows Blue
            secondary = (255, 255, 255, 255) # White
            bg_fill = (255, 255, 255, 255) # White
            
        # MAXIMIZED DIMENSIONS (Full Bleed)
        # Calendar (Left/Back)
        cal_rect = [4, 20, 210, 250] # Almost touching edges
        
        # Draw calendar body
        draw.rounded_rectangle(cal_rect, radius=24, fill=bg_fill, outline=primary, width=12)
        
        # Draw calendar header
        header_height = 70
        draw.rounded_rectangle([cal_rect[0], cal_rect[1], cal_rect[2], cal_rect[1] + header_height], 
                             radius=24, fill=primary, corners=(True, True, False, False))
        # Fix bottom corners of header
        draw.rectangle([cal_rect[0], cal_rect[1] + header_height - 12, cal_rect[2], cal_rect[1] + header_height], fill=primary)
        
        # Calendar lines (minimalist text)
        line_x_start = cal_rect[0] + 30
        line_x_end = cal_rect[2] - 30
        draw.line([line_x_start, 130, line_x_end, 130], fill=primary, width=12)
        draw.line([line_x_start, 170, line_x_end, 170], fill=primary, width=12)
        draw.line([line_x_start, 210, line_x_start + 80, 210], fill=primary, width=12)

        # Clock (Right/Front) - Maximum overlap
        clock_center = (176, 176)
        clock_radius = 76
        clock_bbox = [
            clock_center[0] - clock_radius,
            clock_center[1] - clock_radius,
            clock_center[0] + clock_radius,
            clock_center[1] + clock_radius
        ]
        
        # Clock face
        draw.ellipse(clock_bbox, fill=primary, outline=secondary, width=10)
        
        # Clock hands
        # Hour hand
        draw.line([clock_center, (clock_center[0], clock_center[1] - 50)], fill=secondary, width=12)
        # Minute hand
        draw.line([clock_center, (clock_center[0] + 40, clock_center[1])], fill=secondary, width=10)
        
        # Center dot
        draw.ellipse([clock_center[0]-10, clock_center[1]-10, clock_center[0]+10, clock_center[1]+10], fill=secondary)
        
        return img

    # Generate Normal Icon
    img_normal = draw_icon(is_paused=False)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img_normal.save('icon.ico', format='ICO', sizes=icon_sizes)
    print("Generated icon.ico (Larger)")
    
    # Generate Paused Icon
    img_paused = draw_icon(is_paused=True)
    img_paused.save('icon_paused.ico', format='ICO', sizes=icon_sizes)
    print("Generated icon_paused.ico")
    
    # Save PNG for Landing Page (Normal)
    img_normal.save('dahora_icon.png', format='PNG')
    print("Generated dahora_icon.png")

if __name__ == "__main__":
    create_icons()
