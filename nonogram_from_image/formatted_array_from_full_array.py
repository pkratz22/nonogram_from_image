def get_num_rows(array):
    """Get number of rows that have col data"""
    row_number = 0
    for cell in range(len(array[row_number])):
        if array[row_number][cell] != "":
            if array[row_number + 1][cell] != "":
                row_number += 1
                cell = 0                
            else:
                return (row_number + 1)


def get_num_cols(array):
    """Get number of cols that have row data"""
    row_number = 0
    for cell in range(len(array[row_number])):
        if array[row_number][cell] != "":
            if array[row_number + 1][cell] != "":
                row_number += 1
                cell = 0                
            else:
                return (row_number + 1)


def main(array):
    transposed_array = list(zip(array))
    num_rows = get_num_rows(array)
    num_cols = get_num_cols(transposed_array)
    pass


if __name__ == "__main__":
    array = input("Please enter array: ")
    main(array)