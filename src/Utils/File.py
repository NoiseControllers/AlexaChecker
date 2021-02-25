
import xlsxwriter


def read_file(path: str) -> list:
    temp = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            temp.append(line.strip())

    return temp


def output_file(filename: str, data_list: list):
    outfile = xlsxwriter.Workbook(filename)
    sheet = outfile.add_worksheet()

    header_format = outfile.add_format({'bold': True, 'align': 'left'})
    cell_format = outfile.add_format({'align': 'left', 'num_format': '#,##'})
    sheet.set_column(0, 0, 80)
    sheet.set_column(1, 1, 10)
    sheet.write("A1", "URL", header_format)
    sheet.write("B1", "Alexa", header_format)

    for pos, item in enumerate(data_list):
        sheet.write(pos+1, 0, item[0])
        sheet.write(pos+1, 1, item[1], cell_format)

    outfile.close()
