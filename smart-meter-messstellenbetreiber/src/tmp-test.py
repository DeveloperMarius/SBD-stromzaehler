from datetime import datetime

date_string = "2023-02-12"

print(round(datetime.strptime(date_string, '%Y-%m-%d').timestamp() * 1000))
