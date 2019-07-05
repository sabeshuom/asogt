
import xlsxwriter
import re
import xlrd
import string
alpha_l = string.ascii_lowercase
alpha_u = string.ascii_uppercase


rooms_oral = [{"room": "Room 1", "comps": []},
              {"room": "Room 2", "comps": []},
              {"room": "Room 3"},
              {"room": "Room 4"},
              {"room": "Room 5"},
              {"room": "Room 6"},
              {"room": "Room 7"},
              {"room": "Room 8"},
              {"room": "Room 9"},
              ]

rooms_written = [{"room": "Room 1"},
                 {"room": "Room 2"},
                 {"room": "Room 3"}]


def add_time_table(wb, ws, start_time, comps,  stats_ref_range, total_time_col, comp_type="oral"):
    # total_time_col = 9
    # data_range = "stats!$A$1:$H$40"
    # start_time = "1:30 PM"
    global alpha_u
    rows_per_room = 10
    columns_per_room = 3
    room_split = 3  # grid for room
    top_c = 4
    top_r = 0
    header_rows = 3
    gap_between_rooms = 1

    if comp_type == "oral":
        rooms = rooms_oral
    elif comp_type == "written":
        rooms = rooms_written
    else:
        print("Not implemented error")

    cell_room_format = wb.add_format({
        'bg_color': '#0F2060',
        'font_color': 'white',
        'font_size': 14,
        'font_name': 'Calibri (Body)',
        'bold': 1,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter'
    })

    header_format = wb.add_format({
        'font_size': 14,
        'font_name': 'Calibri (Body)',
        'bold': 1,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter'
    })

    time_format = wb.add_format({
        'font_size': 14,
        'font_name': 'Calibri (Body)',
        'num_format': "hh:mm AM/PM",
        'border': 1,
        'bold': 1
    })

    comp_format = wb.add_format({
        'font_size': 14,
        'bg_color': "#ffe6cc",  # F9CAA4",
        'font_name': 'Calibri (Body)',
        'num_format': "hh:mm AM/PM",
        'border': 1,
        'bold': 1,
        'align': 'left'
    })

    comp_plain_format = wb.add_format({
        'font_size': 14,
        'bg_color': "white",
        'font_name': 'Calibri (Body)',
        'border': 1,
        'bold': 1,
        'align': 'left'
    })

    # Add a format. Green fill with dark green text.
    comp_matched_format = wb.add_format({
        'font_size': 14,
        'font_color': "#006100",
        'bg_color': "#C6EFCE",
        'font_name': 'Calibri (Body)',
        'border': 1,
        'bold': 1,
        'align': 'left'
    })

    # Add a format. Light red fill with dark red text.
    comp_duplicate_format = wb.add_format({
        'font_size': 14,
        'bg_color': "#FFC7CE",
        'font_color': "#9C0006",
        'font_name': 'Calibri (Body)',
        'border': 1,
        'bold': 1
    })
    ws.merge_range("A2:C2", "Comps to Allocate", header_format)
    ws.write_row(2, 0, ["Comp", "Count", "Time"], header_format)  # 3rd row

    data_range_start = "${:s}${:d}".format(
        alpha_u[top_c], top_r + header_rows + 1)
    # ws.conditional_format('A1:A4', {'type':     'formula',
    #                                    'criteria': '=$A$1>5',
    #                                    'format':   comp_duplicate_format})
    comp_alloc_cols = 4  # compettins allocation columns
    data_range_finish = "${:s}${:d}".format(alpha_u[(columns_per_room + 1) * room_split + comp_alloc_cols -1], ((
        len(rooms)/room_split)) * (rows_per_room + header_rows + gap_between_rooms))
    for r, comp_item in enumerate(comps.items()):
        comp = comp_item[0]
        count = comp_item[1][0]
        time = comp_item[1][1]
        cell = "$A${:d}".format(r + header_rows + 1)
        ws.write(cell, comp, comp_plain_format)
        cell_range = "A{:d}:C{:d}".format(
            r + header_rows + 1, r + header_rows + 1)
        ws.conditional_format(cell_range, {'type':     'formula',
                                           'criteria': '=countif({:s}:{:s}, {:s}) = 1'.format(data_range_start, data_range_finish, cell),
                                           'format':   comp_matched_format})
        ws.conditional_format(cell_range, {'type':     'formula',
                                           'criteria': '=countif({:s}:{:s}, {:s}) > 1'.format(data_range_start, data_range_finish, cell),
                                           'format':   comp_duplicate_format})
        ws.write("B{:d}".format(r + header_rows + 1), count, comp_plain_format)
        ws.write("C{:d}".format(r + header_rows + 1), time, comp_plain_format)

    ws.set_column('A:C', 15)
    for room_index, room in enumerate(rooms):
        room_name = room.get("room", "Room {:d}".format(room_index))
        room_comps = room.get("comps", [])
        start_c = top_c + room_index % room_split * 4
        start_r = top_r + room_index/room_split * \
            (rows_per_room + header_rows + gap_between_rooms) + 1

        ws.set_column('{:s}:{:s}'.format(
            alpha_u[start_c], alpha_u[start_c + columns_per_room-1]), 15)
        # set start time
        ws.set_row(start_r-1, 25)  # row index starts 0
        start_time_label_cell = "{:s}{:d}".format(alpha_u[start_c], start_r)
        start_time_cell = "{:s}{:d}".format(alpha_u[start_c+1], start_r)
        ws.write(start_time_label_cell, "Start Time", time_format)
        ws.write(start_time_cell, start_time, time_format)

        # set room title
        ws.set_row(start_r, 25)  # row index starts 0
        room_cell = "{:s}{:d}:{:s}{:d}".format(
            alpha_u[start_c], start_r+1, alpha_u[start_c + columns_per_room-1], start_r + 1)
        ws.merge_range(room_cell, room_name, cell_room_format)

        # set time table header
        ws.set_row(start_r+1, 25)  # row index starts 0
        room_cell = "{:s}{:d}:{:s}{:d}".format(
            alpha_u[start_c], start_r+1, alpha_u[start_c + columns_per_room-1], start_r + 1)
        ws.write_row(start_r+1, start_c,
                     ["Comp", "Start Time", "End Time"], cell_room_format)

        # write row
        for count in range(rows_per_room):
            current_row = start_r + count + header_rows
            ws.set_row(current_row - 1, 25)  # row index starts 0
            comp_cell = '{:s}{:d}'.format(alpha_u[start_c + 0], current_row)
            st_cell = "{:s}{:d}".format(alpha_u[start_c+1], current_row)
            et_cell = "{:s}{:d}".format(alpha_u[start_c+2], current_row)
            if (comp_type == "oral") and (count > 0):
                st = '=IF(ISBLANK({:s}), "", {:s})'.format(
                    comp_cell, "{:s}{:d}".format(alpha_u[start_c+2], current_row - 1))
            else:
                st = '=IF(ISBLANK({:s}), "", {:s})'.format(
                    comp_cell, start_time_cell)

            et = '=IF(ISBLANK({:s}),"", MROUND({:s} + TIME(0, VLOOKUP({:s},{:s},{:d},FALSE),0),"0:15"))'.format(
                comp_cell, st_cell, comp_cell, stats_ref_range, total_time_col)
            ws.write(st_cell, st, comp_format)
            ws.write(et_cell, et, comp_format)
            comp = room_comps[count] if len(room_comps) > count else ""
            ws.write(comp_cell, comp, comp_format)


def test_xls_fromatting():
        # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('merge1.xlsx')
    worksheet = workbook.add_worksheet()

    # Increase the cell size of the merged cells to highlight the formatting.
    worksheet.set_column('B:D', 12)
    worksheet.set_row(3, 30)
    worksheet.set_row(6, 30)
    worksheet.set_row(7, 30)

    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    # Merge 3 cells.
    worksheet.merge_range('B1:D1', 'Merged Range', merge_format)

    # Merge 3 cells over two rows.
    worksheet.merge_range('B7:D8', 'Merged Range', merge_format)

    # set functions

    worksheet.write('B3', "=sum(A3, A4)")

    workbook.close()


if __name__ == "__main__":
    wb = xlsxwriter.Workbook('test.xlsx')
    ws = wb.add_worksheet("stats")
    ws = wb.add_worksheet("Time Table 22-07-2018")
    stats_ref_range = "stats!A1:J30"
    total_time_col = 9
    start_time = "09:30 AM"
    comps = {"PP": [20, 30.0], "BP": [30, 40.0], "SpPP": [40, 34.0]}
    add_time_table(wb, ws,  start_time, comps,  stats_ref_range,
                   total_time_col, comp_type="oral")
    ws = wb.add_worksheet("Time Table 05-08-2018")
    add_time_table(wb, ws,  start_time, comps, stats_ref_range,
                   total_time_col, comp_type="written")
    wb.close()
