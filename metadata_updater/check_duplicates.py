import xml.etree.ElementTree as ET
import os
import csv
import logging

logging.basicConfig(level=logging.INFO)

output_dir = 'C:/Users/ECheng/OneDrive - Land Information New Zealand/Desktop/Repo/Output' 
files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.iso.xml')]  # get a list of all .iso files in the Output directory

def extract_guid(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        namespace_gmd = '{http://www.isotc211.org/2005/gmd}'
        namespace_gco = '{http://www.isotc211.org/2005/gco}'
        file_identifier = root.find(f'{namespace_gmd}fileIdentifier')
        guid = file_identifier.find(f'{namespace_gco}CharacterString').text
        return guid
    except Exception as e:
        print(f"Error parsing file {file_path}: {str(e)}")
        return None

def find_duplicates(files):
    unique_guids = set()
    duplicate_guids = {}
    guid_to_layer = {}
    errors = []

    for file in files:
        guid = extract_guid(file)
        if guid:
            layer_name = os.path.basename(file).replace('.iso.xml', '')
            if guid in unique_guids:
                if guid not in duplicate_guids:
                    duplicate_guids[guid] = [guid_to_layer[guid]]
                duplicate_guids[guid].append(layer_name)
            else:
                unique_guids.add(guid)
                guid_to_layer[guid] = layer_name
        else:
            errors.append((file, 'Error parsing GUID'))

    return duplicate_guids, errors

# Export duplicates to CSV
def export_duplicates_to_csv(duplicate_guids, errors):
    with open('duplicates.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['GUID', 'Layer Names', 'Error Message']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        
        for guid, layer_names in duplicate_guids.items():
            for layer_name in layer_names:
                writer.writerow([guid, layer_name, ''])

        for file_path, error in errors:
            writer.writerow(['', file_path, error])

def main():
    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.iso.xml')]
    duplicate_guids, errors = find_duplicates(files)
    export_duplicates_to_csv(duplicate_guids, errors)
    logging.info("Duplicates exported to duplicates.csv")

if __name__ == '__main__':
    main()