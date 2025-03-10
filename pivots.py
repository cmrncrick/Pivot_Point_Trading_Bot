import time as t
from datetime import datetime, timedelta

from helpers.constants import INTERVAL_15M, LOOKBACK_PERIOD, TICKER
from helpers.functions import (curr_price, data_retrieval, date_transform,
                               pivots, send_discord_msg)

df = data_retrieval(days_lookback=LOOKBACK_PERIOD,
                    ticker=TICKER, interval=INTERVAL_15M)

df = date_transform(df)

# Extract pivot levels
pivot_levels = {
    "PP": None,
    "R1": None, "R2": None, "R3": None,
    "S1": None, "S2": None, "S3": None
}

pivot_levels["PP"], pivot_levels["R1"], pivot_levels["R2"], pivot_levels["R3"], \
    pivot_levels["S1"], pivot_levels["S2"], pivot_levels["S3"] = pivots(df)

# Not sure I need to wait any amount of time unless I schedule for a certain time and then don't run until market open
# now = datetime.now()

# # Next full minute
# next_minute = (now + timedelta(minutes=1)
#                ).replace(second=0, microsecond=0)

# time_to_wait = (next_minute - now).total_seconds()

# t.sleep(time_to_wait)

while True:
    #################################################################################################
    # YFinance pulling delayed data
    #################################################################################################
    price = curr_price(TICKER)
    print(price)

    # Check if price is within 2.00 of any pivot level and capture the matching level
    triggered_levels = [
        name for name, level in pivot_levels.items() if abs(price - level) <= 2.00
    ]
#################################################################################################
# Trigger will constantly repeat. Need debounce after first message.
#################################################################################################
    if triggered_levels:
        content = (
            f"Triggered! Price: {price} is within 2.00 of {', '.join(triggered_levels)}")
        send_discord_msg(content)

    t.sleep(2)
