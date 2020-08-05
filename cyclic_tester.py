
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

f = open('cron_test.txt', 'a')
f.write('Check at ' + str(current_time) +'\n')
f.close()