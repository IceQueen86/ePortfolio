## Enhancement 2: Create Custom In-Memory QuickSort Routine Executes an optimized 
## divide-and-conquer sorting strategy over an array of dictionary documents 
## based on a user-selected attribute. 

## Average-Time Complexity: O(n log n)
## Space Complexity: O(n) due to recursion stack partitions

def quicksort_records(records_list, key_attribute):

    # DEFENSIVE PROGRAMMING: Core base case condition checks for empty or single-item lists
    if len(records_list) <= 1:
        return records_list

    # Initialize partition storage lists
    left_partition = []
    middle_partition = []
    right_partition = []

    # Choose the middle element as the structural pivot point
    pivot_record = records_list[len(records_list) // 2]
    
    # DEFENSIVE PROGRAMMING: Handle missing key errors gracefully using .get() fallbacks
    pivot_val = pivot_record.get(key_attribute, 0)

    # Sort and partition elements sequentially into corresponding array groups
    for record in records_list:
        current_val = record.get(key_attribute, 0)
        
        # Logic construct splits the elements relative to the chosen pivot values
        if current_val < pivot_val:
            left_partition.append(record)
        elif current_val == pivot_val:
            middle_partition.append(record)
        else:
            right_partition.append(record)

    # Recursively sort left and right partitions, then combine the final results
    return quicksort_records(left_partition, key_attribute) + middle_partition + quicksort_records(right_partition, key_attribute)
