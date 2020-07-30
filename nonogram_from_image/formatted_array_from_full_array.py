"""Convert array of entire grid to row/col arrays

Functions:
    get_num_rows(array)
    get_num_cols(array)
"""


def get_num_rows(grid_array):
    """Get number of rows that have col data"""
    row_number = 0
    for cell in range(len(grid_array[row_number])):
        if grid_array[row_number][cell] != "":
            if grid_array[row_number + 1][cell] != "":
                row_number += 1
                cell = 0
    return row_number


def get_num_cols(grid_array):
    """Get number of cols that have row data"""
    row_number = 0
    for cell in range(len(grid_array[row_number])):
        if grid_array[row_number][cell] != "":
            if grid_array[row_number + 1][cell] != "":
                row_number += 1
                cell = 0
    return row_number


def get_col_array(grid_array, num_rows):
    """Get col array from grid"""
    return


def get_row_array(grid_array, num_cols):
    """Get row array from grid"""
    return


def main(grid_array):
    """Given grid_array, return teal array"""
    transposed_array = list(zip(grid_array))
    num_rows = get_num_rows(grid_array)
    num_cols = get_num_cols(transposed_array)
    col_array = get_col_array(transposed_array, num_rows)
    pass


if __name__ == "__main__":
    array = input("Please enter array: ")
    main(array)
