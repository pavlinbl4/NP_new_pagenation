from openpyxl.utils import get_column_letter


def set_column_dimensions(worksheet, columns_width: list):
    for column_number, column_width in enumerate(columns_width, start=1):
        worksheet.column_dimensions[f'{get_column_letter(column_number)}'].width = column_width
    return worksheet
