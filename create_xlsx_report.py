"""
Из скачанных парсером снимков нового проспекта за месяц генерю
файл отчета с превью
"""
from pathlib import Path
from openpyxl import Workbook

from datetime import datetime
from openpyxl.utils import get_column_letter
from files_and_folders.folder_in_MY_documents import make_documents_folder
from openpyxl.styles import (
    Border, Side,
    Alignment, Font
)
from parsing.image_resize import image_resize
from gui_tools.select_month import select_month
from xlsx_tools.set_column_dimensions import set_column_dimensions

from loguru import logger

month_name = select_month()
current_year = datetime.now().year

way_to_files = Path(
    f"{make_documents_folder('NewProspect')}/{current_year}_{month_name}")  # путь к папке с изображениями

workbook = Workbook()
worksheet = workbook.active
worksheet.title = "Sheet with image"  # задаю название вкладки

# in list widths of all columns
worksheet = set_column_dimensions(worksheet, [30, 600, 40, 30])

thin_border = Border(left=Side(border_style="thin"),
                     right=Side(border_style="thin"),
                     top=Side(border_style="thin"),
                     bottom=Side(border_style="thin"))
# worksheet.row_dimensions.defaultRowHeight = 130

row = 0

for row, image_path in enumerate(way_to_files.glob("*.JPG"), 1):
    worksheet.row_dimensions[row].height = 130  # задаю высоту столбца

    logger.info(image_path)
    img = image_resize(image_path)

    for column in range(1, 5):
        # cells view
        worksheet[f'{get_column_letter(column)}{row}'].border = thin_border
        worksheet[f'{get_column_letter(column)}{row}'].font = Font(size=20, bold=True)
        worksheet[f'{get_column_letter(column)}{row}'].alignment = Alignment(horizontal='center',
                                                                             vertical='center',
                                                                             wrap_text=True)
        worksheet[f'{get_column_letter(3)}{row}'].alignment = Alignment(horizontal='center',
                                                                        vertical='center',
                                                                        )
        # add information to cells

        worksheet[f'{get_column_letter(1)}{row}'].value = image_path.name.split("__")[0]
        worksheet[f'{get_column_letter(2)}{row}'].value = image_path.name.split("__")[1][:-4]
        # logger.info(img)
        worksheet.add_image(img, f"{get_column_letter(3)}{row}")
        worksheet[f'{get_column_letter(4)}{row}'].value = 500

for column in range(1, 5):
    worksheet[f'{get_column_letter(column)}{row + 3}'].alignment = Alignment(horizontal='center', vertical='center')
    worksheet[f'{get_column_letter(column)}{row + 3}'].font = Font(size=32, bold=True, color="FF0000")
    worksheet[f'{get_column_letter(column)}{row + 3}'].border = thin_border

    worksheet.row_dimensions[row + 3].height = 60
    worksheet[f'{get_column_letter(2)}{row + 3}'].value = "ИТОГО"
    worksheet[f'{get_column_letter(4)}{row + 3}'].value = f"=SUM(D$1:D${row})"

workbook.save(f"{way_to_files}/report_{current_year}_{month_name}.xlsx")
workbook.close()
