#! /usr/bin/python
"""
Copyright 2021 Andreas Finkler

This small script parses the log output of pmset to calculate how long the laptop was actively used since it
was last unplugged from the AC.
"""

import subprocess
import re
import sys
from datetime import datetime

timestamp = r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s[+-]\d{4}"
display_switched = re.compile(timestamp + "\s+\w+\s+Display is turned (?P<state>\w+)")
charge_on_ac = re.compile(timestamp + "\s+\w+\s+.*Using AC \(Charge:(?P<charge>\d+)%\)")

timestamp_format = "%Y-%m-%d %H:%M:%S"

raw_output = subprocess.check_output(["pmset", "-g", "log"])
if sys.version_info.major >= 3:
    pmset_log = str(raw_output, "utf-8")
else:
    pmset_log = raw_output

last_charge_timestamp, last_charge_value = charge_on_ac.findall(pmset_log)[-1]
all_times = display_switched.findall(pmset_log)
display_times = [
    status 
    for status in all_times 
    if datetime.strptime(status[0], timestamp_format) >= datetime.strptime(last_charge_timestamp, timestamp_format)
]
last_state_before_full_charge = all_times[-len(display_times)-1]
durations = []
last_on = datetime.strptime(last_charge_timestamp, timestamp_format)
current_state = last_state_before_full_charge[-1]
for entry in display_times:
    if entry[-1] == "on" and current_state == "off":
        last_on = datetime.strptime(entry[0], timestamp_format)
    elif entry[-1] == "off" and current_state == "on":
        durations.append((datetime.strptime(entry[0], timestamp_format) - last_on).total_seconds())
    current_state = entry[-1]
# current time
durations.append((datetime.now() - last_on).total_seconds())
print("Last charge was to {}%, since then actively used for {:.2f} hours".format(last_charge_value, sum(durations) / 60 / 60))
