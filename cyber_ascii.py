import sys
import random
from PIL import Image, ImageDraw, ImageFont

def image_to_ascii_frames(image_path, output_path="profile_ascii.gif", width=80, frames_count=40):
    try:
        img = Image.open(image_path).convert('L')
    except Exception as e:
        print(f"Hata: Görüntü açılamadı - {e}")
        return

    aspect_ratio = img.height / img.width
    new_height = int(aspect_ratio * width * 0.55)
    img = img.resize((width, new_height))
    pixels = img.load()

    chars = ['#', '@', '%', '=', '+', '*', ':', '-', '.', ' ']
    
    final_grid = []
    for y in range(new_height):
        row = []
        for x in range(width):
            pixel_val = pixels[x, y]
            char_index = int((pixel_val / 255) * (len(chars) - 1))
            row.append(chars[char_index])
        final_grid.append(row)

    try:
        font = ImageFont.truetype("consola.ttf", 12)
    except IOError:
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", 12)
        except IOError:
            font = ImageFont.load_default()

    try:
        left, top, right, bottom = font.getbbox("A")
        char_width, char_height = right - left, bottom - top
    except AttributeError:
        char_width, char_height = 6, 12

    canvas_width = width * char_width
    canvas_height = int(new_height * char_height * 1.2)

    all_positions = [(x, y) for x in range(width) for y in range(new_height)]
    random.shuffle(all_positions)
    
    chunk_size = len(all_positions) // frames_count

    revealed = set()
    frames = []

    print("Siberpunk animasyon kareleri (frames) oluşturuluyor...")
    for i in range(frames_count):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < frames_count - 1 else len(all_positions)
        revealed.update(all_positions[start_idx:end_idx])

        frame_img = Image.new('RGB', (canvas_width, canvas_height), color=(13, 17, 23))
        draw = ImageDraw.Draw(frame_img)

        for y in range(new_height):
            for x in range(width):
                if (x, y) in revealed:
                    char = final_grid[y][x]
                    draw.text((x * char_width, int(y * char_height * 1.2)), char, font=font, fill=(0, 255, 255))
        
        frames.append(frame_img)
        
    for _ in range(15):
        frames.append(frames[-1])

    print(f"{output_path} olarak kaydediliyor...")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0
    )
    print("Sistem Hazır! GIF başarıyla oluşturuldu.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python cyber_ascii.py <fotograf_adi.jpg/png>")
    else:
        in_img = sys.argv[1]
        out_img = "profile_ascii.gif"
        image_to_ascii_frames(in_img, out_img)
