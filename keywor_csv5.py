from collections import defaultdict, deque
import csv

# Function to search for keywords in a source CSV and copy rows to a template CSV
def search_and_copy(source_file, template_file, keywords, search_column, location_col_name, switch_col_name):
    # Nested defaultdict to store rows organized by location and switch
    location_switch_data = defaultdict(lambda: defaultdict(list))
    
    # Variable to store column headers from the source file
    headers = None
    
    # Flag to indicate whether headers have already been added to the template
    headers_added = False

    # Reading the source CSV file
    with open(source_file, 'r') as infile:
        csv_reader = csv.DictReader(infile)
        headers = csv_reader.fieldnames  # Save headers from the source file
        for row in csv_reader:
            # Checking if any keyword exists in the specified search column
            if any(keyword.lower() in row[search_column].lower() for keyword in keywords):
                location = row[location_col_name]
                switch = row[switch_col_name]
                location_switch_data[location][switch].append(row)

    # Loop through each location and switch to process rows
    for location, switches in location_switch_data.items():
        for switch, rows in switches.items():
            # Reading the template CSV into a list
            with open(template_file, 'r') as tmplfile:
                template_reader = csv.reader(tmplfile)
                template_content = list(template_reader)

            # Mapping keywords to corresponding row indices in the template file
            keyword_to_template_indices = defaultdict(deque)
            for idx, template_row in enumerate(template_content):
                for keyword in keywords:
                    if keyword.lower() in str(template_row).lower():
                        keyword_to_template_indices[keyword.lower()].append(idx)

            # Adding headers to the first row of the template only once
            if not headers_added:
                template_content[0].extend(headers)
                headers_added = True

            # Appending rows from the source file to the template
            for row in rows:
                for keyword in keywords:
                    if keyword.lower() in row[search_column].lower():
                        if keyword_to_template_indices[keyword.lower()]:
                            idx = keyword_to_template_indices[keyword.lower()].popleft()
                            template_content[idx].extend(list(row.values()))

            # Writing the updated rows back to a new template file
            output_filename = f"{location}_{switch}_{template_file}"
            with open(output_filename, 'w', newline='') as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerows(template_content)

# Keywords to search for in the source file
keywords_to_search = ['keyword1', 'keyword2']

# Source and template CSV filenames
source_file_name = "source.csv"
template_file_name = "template.csv"

# Column names for location and switch identifiers in the source file
location_column_name = 'Location'
switch_column_name = 'SwitchName'

# Column name where keywords are to be searched
search_column_name = 'Description'

# Execute the search and copy function
search_and_copy(source_file_name, template_file_name, keywords_to_search, search_column_name, location_column_name, switch_column_name)
