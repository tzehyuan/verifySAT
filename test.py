def convert_list_of_lists_to_string(list_of_lists):
    # Initialize an empty list to hold the string elements
    result_list = []
    # Iterate through each sublist
    for sublist in list_of_lists:
        # Convert each sublist to a string
        sublist_str = ', '.join(map(str, sublist))
        # Append the sublist string to the result list
        result_list.append(f'[{sublist_str}]')
    # Join all sublist strings with a comma and space
    result_string = ', '.join(result_list)
    # Return the formatted string
    return f'[{result_string}]'

# Example usage
list_of_lists = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
result_string = convert_list_of_lists_to_string(list_of_lists)
print(result_string)  # Output: '[[1, 2, 3], [4, 5], [6, 7, 8, 9]]'
s = [[1,2,3]]
s.extend([[23]])
print(s)