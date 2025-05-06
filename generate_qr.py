import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

csv_file = 'contacts.csv'  
output_folder = 'qr_codes'  
qr_fill_color = "black"
qr_back_color = "white"    
add_padding = True         
padding_size = 30          
use_logo = True            
logo_path = 'logo.png'     

font_path = "Montserrat-Bold.ttf"
base_font_size = 36
max_text_width_ratio = 0.95
text_color = "#008eb9"

data = pd.read_csv(csv_file, dtype={'Phone': str}, sep=';', encoding='latin1')

os.makedirs(output_folder, exist_ok=True)

def fit_text_width(text, font_path, initial_size, max_width):
    font_size = initial_size
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getbbox(text)[2] - font.getbbox(text)[0]
    while text_width > max_width and font_size > 10:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        text_width = font.getbbox(text)[2] - font.getbbox(text)[0]
    return font

def add_logo_and_name(qr_img, logo_path, full_name, title):
    qr_width, qr_height = qr_img.size
    logo = Image.open(logo_path).convert("RGBA")

    logo_size_ratio = 0.5
    logo_width = int(qr_width * logo_size_ratio)
    logo_height = int(logo.size[1] * (logo_width / logo.size[0]))
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    display_name = f"{full_name} | {title.upper()}"
    font = fit_text_width(display_name, font_path, base_font_size, int(qr_width * max_text_width_ratio))

    text_width = font.getbbox(display_name)[2] - font.getbbox(display_name)[0]
    ascent, descent = font.getmetrics()
    text_height = ascent + descent + 10  

    spacing_logo_qr = 10
    spacing_qr_text = 10  
    total_height = logo_height + spacing_logo_qr + qr_height + spacing_qr_text + text_height

    new_img = Image.new('RGB', (qr_width, total_height), "white")
    new_img.paste(logo, (qr_width // 2 - logo.size[0] // 2, 0), mask=logo)
    new_img.paste(qr_img, (qr_width // 2 - qr_img.size[0] // 2, logo_height + spacing_logo_qr))

    draw = ImageDraw.Draw(new_img)
    text_position_y = logo_height + spacing_logo_qr + qr_height + spacing_qr_text
    text_position = ((qr_width - text_width) // 2, text_position_y)
    draw.text(text_position, display_name, font=font, fill=text_color)

    return new_img

for index, row in data.iterrows():
    full_name = row['Full Name']
    phone = row['Phone'].strip("'")
    email = row['Email']
    department = row.get('Department', '')
    company = row.get('Company', '')
    
    
    street = row.get('Street', '')
    city = row.get('City', '')
    
    
    city_sanitized = city.strip().replace(' ', '_') or "UnknownCity"
    city_folder = os.path.join(output_folder, city_sanitized)
    os.makedirs(city_folder, exist_ok=True)

    state = row.get('State', '')
    zip_code = row.get('Zip', '')
    country = row.get('Country', '')

    
    address = f"{street};{city};{state};{zip_code};{country}"

    if not phone.startswith('+'):
        phone = '+' + phone

    website = "https://www.config.ba"

    # Split full name for N: field
    name_parts = full_name.strip().split()
    last_name = name_parts[-1] if len(name_parts) > 1 else ''
    first_name = ' '.join(name_parts[:-1]) if len(name_parts) > 1 else name_parts[0]

    

    # vCard format
    vcard = f"""BEGIN:VCARD
VERSION:4.0
N:{last_name};{first_name};;;
FN:{full_name}
ORG:{company}
TITLE:{department}
TEL;TYPE=CELL:{phone}
EMAIL:{email}
ADR:;;{address};;;;
URL:{website}
END:VCARD"""

  
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)

    img = qr.make_image(fill_color=qr_fill_color, back_color=qr_back_color).convert('RGB')

    if use_logo and os.path.exists(logo_path):
        img = add_logo_and_name(img, logo_path, full_name, department)

    if add_padding:
        padded_img = Image.new("RGB", (img.size[0] + padding_size * 2, img.size[1] + padding_size * 2), "white")
        padded_img.paste(img, (padding_size, padding_size))
        img = padded_img

    filename = f"{full_name.replace(' ', '_')}_{phone}.png"
    img.save(os.path.join(city_folder, filename))

    print(f"✅ Created QR for {full_name}")

print("\n🎯 All QR codes generated successfully!")
