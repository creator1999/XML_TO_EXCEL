import xml.etree.ElementTree as ET
import pandas as pd


# Recursive function to calculate the maximum depth of the XML tree
def find_max_depth(element, level=0):
    if not list(element):
        return level
    return max(find_max_depth(child, level + 1) for child in element)


# Load and parse the XML file
file = 'hr_data.xml'  # Replace with your XML file
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

# Convert dictionaries to DataFrames and join them on a common key
# For this example, let's assume there's a common key like 'id' or 'name'
merged_df = None
common_key = 'id'  # Specify the column name for joining (modify as per your data)

for idx, dic in enumerate(list_dict):
    # Convert dictionary to DataFrame
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dic.items()]))

    # Join DataFrames on the common key
    if common_key in df.columns:
        if merged_df is None:
            merged_df = df  # Initialize with the first DataFrame
        else:
            merged_df = pd.merge(merged_df, df, on=common_key, how='outer')  # Outer join to combine all keys

# Write the merged DataFrame to Excel
with pd.ExcelWriter(file+"xlsx", engine='openpyxl') as writer:
    # Save the final merged DataFrame to one sheet
    merged_df.to_excel(writer, sheet_name='MergedData', index=False)

    # Formatting for column width
    workbook = writer.book
    worksheet = writer.sheets['MergedData']
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

print("Merged data has been saved to 'output_hr_data_merged.xlsx'")
