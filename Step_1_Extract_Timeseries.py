'''
Extract timeseries from the locally-stored nsidc0766 geotiffs and save them into a csv file for easy reading later.
There is probably a smarter way to do this.
'''
import os
import csv
import rasterio
from rasterio.errors import RasterioIOError
from datetime import datetime
from tqdm import tqdm

# Directory containing the TIFF files
directory = '/data/fast1/nsidc0766/downloaded_files'

# Output CSV file
output_csv = 'jakobshavn.csv'

# Range of x and y coordinates
x_range = range(2500, 2510)  # Adjust this range as needed
y_range = range(8200, 8210)  # Adjust this range as needed

def parse_date(date_str):
    """ Parse the date from filename format DDMMMYY to YYYY-MM-DD """
    return datetime.strptime(date_str, "%d%b%y").strftime("%Y-%m-%d")

# Generate headers based on x, y combinations
headers = ['Date'] + [f'Pixel Value (x={x}, y={y})' for x in x_range for y in y_range]

# Open the output CSV file for writing
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    # Collect all tif files
    tif_files = [f for f in os.listdir(directory) if f.endswith('.tif')]
    
    # Iterate over each file in the directory with a progress bar
    for filename in tqdm(tif_files, desc="Processing TIFF files"):
        # Extract the date from the filename
        parts = filename.split('_')
        date_str = parts[4]  # Correctly pick the starting date part
        date_formatted = parse_date(date_str)

        # Construct the full path to the file
        filepath = os.path.join(directory, filename)

        try:
            # Open the TIFF file
            with rasterio.open(filepath) as src:
                # Prepare row with the date and pixel values
                row = [date_formatted]
                for x in x_range:
                    for y in y_range:
                        value = src.read(1)[y, x]  # Read the value at each x, y coordinate
                        row.append(value)

                # Write the row to the CSV
                writer.writerow(row)
        except RasterioIOError as e:
            print(f"Failed to process {filename}: {e}")
        except IndexError:
            print(f"Pixel coordinates out of bounds for {filename}")
        except Exception as e:
            print(f"An unexpected error occurred with {filename}: {e}")

print("Processing complete. Data written to", output_csv)