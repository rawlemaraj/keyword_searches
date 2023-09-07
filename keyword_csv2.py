# n this modified script, I added an additional argument called search_column to the search_and_copy function. 
# This specifies which column to search for the keywords. The keywords themselves are now specified in a list called keywords_to_search.
# All the other functionalities and debugging print statements are retained from the previous version of the script.

import csv
from collections import defaultdict

def search_and_copy(source_file, template_file, keywords, search_column, location_col_name, switch_col_name):
    location_switch_data = defaultdict(lambda: defaultdict(list))

    print("Starting to read source file...")

    # Read the source file to search for keywords and collect rows by location and switch
    with open(source_file, 'r') as infile:
        csv_reader = csv.DictReader(infile)

        for row in csv_reader:
            if any(keyword.lower() in row[search_column].lower() for keyword in keywords):
                print(f"Found matching row: {row}")
                location = row[location_col_name]
                switch = row[switch_col_name]

                location_switch_data[location][switch].append(row)

    print(f"Completed reading source file. Data organized by {len(location_switch_data)} locations.")

    # Go through each location and switch, and modify the template
    for location, switches in location_switch_data.items():
        print(f"Processing location: {location}")
        for switch, rows in switches.items():
            print(f"Processing switch: {switch}")

            # Read the template file to get the content
            with open(template_file, 'r') as tmplfile:
                print("Reading template file...")
                template_reader = csv.reader(tmplfile)
                template_content = list(template_reader)

            # Update the template_content with rows from the source file
            for row in rows:
                print(f"Updating template with row: {row}")
                for idx, template_row in enumerate(template_content):
                    if any(keyword.lower() in str(cell).lower() for keyword in keywords for cell in template_row):
                        template_content[idx].extend(list(row.values()))
                        print(f"Updated row {idx} in template")

            # Write the updated template content to a new CSV file
            output_filename = f"{location}_{switch}_{template_file}"
            with open(output_filename, 'w', newline='') as outfile:
                print(f"Writing updated data to {output_filename}")
                csv_writer = csv.writer(outfile)
                csv_writer.writerows(template_content)
            print(f"Completed writing to {output_filename}")

# Keywords to search for in a specific column
keywords_to_search = ['keyword1', 'keyword2']  # Add more keywords here

# Source CSV file
source_file_name = "source.csv"

# Template CSV file
template_file_name = "template.csv"

# Column names in the source CSV file that contain the location and switch identifiers
location_column_name = 'Location'
switch_column_name = 'SwitchName'

# Column name in which to search for the keywords
search_column_name = 'ColumnNameToSearch'

# Perform the search and copy operation
print("Starting the search and copy operation...")
search_and_copy(source_file_name, template_file_name, keywords_to_search, search_column_name, location_column_name, switch_column_name)
print("Search and copy operation completed.")
