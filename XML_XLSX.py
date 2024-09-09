import xml.etree.ElementTree as ET
import pandas as pd

# Recursive function to calculate the maximum depth of the XML tree
def find_max_depth(element, level=0):
    if not list(element):
        return level
    return max(find_max_depth(child, level + 1) for child in element)

# Load and parse the XML file
file = ''  # Replace with your XML file
tree = ET.parse(file)
root = tree.getroot()

# Call the function and get the maximum depth
max_depth = find_max_depth(root)

# Initialize lists to hold elements at each depth
i1 = 0
list_elements = []
list_elements.append(list(root))  # Add the direct children of root

# Collect elements at each depth level
whole_list = [list(root)]
while i1 < max_depth:
    temp_list = []
    for elem in list_elements[i1]:
        temp_list.extend(list(elem))
    whole_list.append(temp_list)
    list_elements.append(temp_list)
    i1 += 1

# Function to merge dictionaries by attribute keys
def merge_dicts(dict_list):
    merged_dicts = []
    for current_dict in dict_list:
        matched = False
        for dic in merged_dicts:
            if set(dic.keys()) == set(current_dict.keys()):
                for key in current_dict:
                    if isinstance(dic[key], list):
                        dic[key].append(current_dict[key])
                    else:
                        dic[key] = [dic[key], current_dict[key]]
                matched = True
                break
        if not matched:
            merged_dicts.append({key: value for key, value in current_dict.items()})
    return merged_dicts

# Create a list of dictionaries from the attributes of elements at all depth levels
list_dict = []
for level in whole_list:
    level_dicts = [elem.attrib for elem in level if elem.attrib]
    list_dict = merge_dicts(list_dict + level_dicts)

# Convert each dictionary into a DataFrame and write all DataFrames to a single Excel sheet
with pd.ExcelWriter('output_hr_data.xlsx', engine='openpyxl') as writer:
    start_row = 0  # To track where to start writing each DataFrame
    sheet_name = 'MergedData'  # Single sheet name

    for idx, dic in enumerate(list_dict):
        # Convert dictionary to DataFrame
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dic.items()]))

        # Write DataFrame to Excel in the same sheet with a gap of 5 rows
        df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False)

        # Leave a gap of 5 rows between each DataFrame
        start_row += len(df) + 6

    # Formatting for column width
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    for column in worksheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

print("Data has been saved.")
