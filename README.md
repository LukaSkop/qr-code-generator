# QR Code Generator for Employee Contacts

This Python script generates personalized QR codes containing vCard information for company employees. The QR codes include contact details such as name, phone, email, department, and address, and can optionally include a logo and styled name below each code.

## Features

- Reads employee data from a `.csv` file
- Generates vCard QR codes (compatible with most phones)
- Optionally adds:
  - Company logo
  - Employee name and department
  - Padding around the QR code
- Saves each QR code image in a city-based subfolder

## Folder Structure

<pre>
qr-code-generator/ 
├── contacts.csv # Employee data (not tracked in Git) 
├── logo.png # Company logo (not tracked in Git) 
├── qr_codes/ # Output folder for generated QR codes (not tracked in Git) 
├── generate_qr_codes.py # Main Python script 
└── README.md</pre>

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/LukaSkop/qr-code-generator.git
   cd qr-code-generator
   ```
2.Install required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

3.Prepare your contacts.csv file with these columns (use ; as the separator):

<pre> Full Name;Phone;Email;Department;Company;Street;City;State;Zip;Country </pre>
  
Add your logo image as logo.png and font as Montserrat-Bold.ttf in the root folder.

## Usage
Run the script:
```bash
python generate_qr_codes.py
  ```
All generated QR codes will be saved inside the qr_codes/ directory, organized by city.

Notes
The QR codes use vCard version 4.0.

Phone numbers will be prefixed with + if not already formatted that way.

contacts.csv and the generated QR images are excluded from Git using .gitignore.

