from collections import defaultdict, deque
import csv

def search_and_copy(source_file, template_file, keywords, search_column, location_col_name, switch_col_name):
    location_switch_data = defaultdict(lambda: defaultdict(list))
    headers = None  # Initialize headers variable

    print("Starting to read source file...")

    with open(source_file, 'r') as infile:
        csv_reader = csv.DictReader(infile)
        headers = csv_reader.fieldnames  # Save headers from source
        for row in csv_reader:
            if any(keyword.lower() in row[search_column].lower() for keyword in keywords):
                print(f"Found matching row: {row}")
                location = row[location_col_name]
                switch = row[switch_col_name]
                location_switch_data[location][switch].append(row)

    print(f"Completed reading source file. Data organized by {len(location_switch_data)} locations.")

    for location, switches in location_switch_data.items():
        print(f"Processing location: {location}")

        for switch, rows in switches.items():
            print(f"Processing switch: {switch}")

            with open(template_file, 'r') as tmplfile:
                print("Reading template file...")
                template_reader = csv.reader(tmplfile)
                template_content = list(template_reader)

            keyword_to_template_indices = defaultdict(deque)
            for idx, template_row in enumerate(template_content):
                for keyword in keywords:
                    if keyword.lower() in str(template_row).lower():
                        keyword_to_template_indices[keyword.lower()].append(idx)

            for row in rows:
                for keyword in keywords:
                    if keyword.lower() in row[search_column].lower():
                        if keyword_to_template_indices[keyword.lower()]:
                            idx = keyword_to_template_indices[keyword.lower()].popleft()
                            # Append headers if this is the first time this row is being updated
                            if len(template_content[idx]) == len(template_content[0]):
                                template_content[idx].extend(headers)
                            template_content[idx].extend(list(row.values()))
                            print(f"Updated row {idx} for keyword: {keyword} in template")

            output_filename = f"{location}_{switch}_{template_file}"
            with open(output_filename, 'w', newline='') as outfile:
                print(f"Writing updated data to {output_filename}")
                csv_writer = csv.writer(outfile)
                csv_writer.writerows(template_content)
            print(f"Completed writing to {output_filename}")

# Keywords to search for in a specific column
keywords_to_search = ['keyword1', 'keyword2']

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
