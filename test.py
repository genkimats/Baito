from datetime import datetime
import pandas as pd

print(datetime.today().strftime("%Y/%m"))
print(pd.to_datetime("22:00", format="%H:%M"))