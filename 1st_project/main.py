import time 
import gspread
import requests

gc = gspread.service_account(filename='key.json')
sh = gc.open("qwe")

worksheet = sh.get_worksheet(0)
link_list = worksheet.col_values(1)
list_without_http_s = []
response_list = []
for ll in link_list:
    a = ll.replace('http://', '').replace('https://', '')
    list_without_http_s.append(a)

cell_list = worksheet.range(f'B1:B{len(link_list)}')

for i,x in enumerate(list_without_http_s):
    while True:
        try:
            time.sleep(3)
            r = requests.get('https://ru.megaindex.com/app/records/live/report/keywords', params={
                                "auth_key":"254925:beae1ccec1512f74b04ba133f3a8a538",
                                "ikey":"3aa68a3dad7ec056d5bf89a11a26bbe0",
                                "out":"json",
                                "domain":x,
                                "lang":"ru",
                            })
            data = r.json()
            response_list.append(data['data']['organic']['traffic'])
            print(i+1, x, data['data']['organic']['traffic'])
            break
        except:
            time.sleep(10)
    if len(response_list)%100 == 0:

        for i, cell in enumerate(cell_list):
            try:
                cell.value = response_list[i]
            except:
                break
        # Update in batch
        worksheet.update_cells(cell_list)

# for i, cell in enumerate(cell_list):
#     cell.value = response_list[i]

# # Update in batch
# worksheet.update_cells(cell_list)

pass