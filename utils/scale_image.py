import datetime



# This function is used to get the scale value based on the creation date of the asset
# Ranging from 0 to 1, the scale value is used to determine how old the asset is. Every day it is decreased by 0.1
# created_at will be like 2024-08-01 07:42:53
def get_scale_value(created_at: str) -> float:
    current_date = datetime.datetime.now()
    created_date = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

    days_difference = (current_date - created_date).days
    scale_value = max(1 - (days_difference * 0.1), 0)
    return scale_value







