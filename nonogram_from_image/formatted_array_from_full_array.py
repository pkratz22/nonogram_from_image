"""Convert array of entire grid to row/col arrays"""


def get_num_rows_cols(grid_array):
    """Get number of rows that have col data"""
    row_number = 0
    is_last_row = False
    while not is_last_row:
        is_last_row = check_if_last_row(grid_array, row_number)
        row_number += 1
    return row_number


def check_if_last_row(grid_array, row_number):
    """Loop through row for get_num_rows_cols"""
    for cell in range(len(grid_array[row_number])):
        if grid_array[row_number][cell] != "":
            if grid_array[row_number + 1][cell] != "":
                return False
    return True


def get_row_col_array(grid_array, rows_skipped):
    """Get col array from grid"""
    ver_hor_array = []
    total_rows = len(grid_array)
    for row in range(rows_skipped, total_rows):
        individual_row_array = []
        for cell in range(len(grid_array[row])):
            if grid_array[row][cell] != "":
                individual_row_array.append(grid_array[row][cell])
        ver_hor_array.append(individual_row_array)
    return ver_hor_array


def get_ver_hor_array_as_string(ver_hor_array):
    """Gets vertical or horizontal array as string"""
    ver_hor_string = '['
    for row_num, _ in enumerate(ver_hor_array):
        ver_hor_string += '['
        for cell in range(len(ver_hor_array[row_num])):
            ver_hor_string += str(ver_hor_array[row_num][cell]) + ','
        ver_hor_string = ver_hor_string[:-1]
        ver_hor_string += '],'
    ver_hor_string = ver_hor_string[:-1]
    ver_hor_string += ']'
    return ver_hor_string


def get_teal_string(vertical, horizontal):
    """Formats string for use in teal online tool"""
    ver_string = get_ver_hor_array_as_string(vertical)
    hor_string = get_ver_hor_array_as_string(horizontal)
    return '{"ver":' + ver_string + ',"hor":' + hor_string + '}'


def main(grid_array):
    """Given grid_array, return teal array"""
    transposed_array = list(map(list, zip(*grid_array)))
    num_rows = get_num_rows_cols(grid_array)
    num_cols = get_num_rows_cols(transposed_array)
    ver_array = get_row_col_array(grid_array, num_cols)
    hor_array = get_row_col_array(transposed_array, num_rows)
    teal_string = get_teal_string(ver_array, hor_array)
    return teal_string


if __name__ == "__main__":
    # array = input("Please enter array: ")
    array = [["", "", "", "", 1, "", "", 1, ""],
                      ["", "", "", "", 1, 4, 4, 1, ""],
                      ["", "", "", 4, 2, 1, 1, 2, 4],
                      ["", "", 4, "", "", "", "", "", ""],
                      [1, 2, 1, "", "", "", "", "", ""],
                      ["", "", 6, "", "", "", "", "", ""],
                      [1, 2, 1, "", "", "", "", "", ""],
                      ["", 2, 2, "", "", "", "", "", ""],
                      ["", "", 4, "", "", "", "", "", ""]]
    print(main(array))
