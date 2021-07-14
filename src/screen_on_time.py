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

TIMESTAMP_REGEX = r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s[+-]\d{4}"


def main():
    pmset_log = get_pmset_log()
    last_charge_timestamp, last_charge_value = get_last_charge_info(pmset_log)
    display_on_duration = get_time_with_display_turned_on(pmset_log, starting_from=last_charge_timestamp)
    hours = int(display_on_duration / 3600)
    minutes = int(display_on_duration % 3600 / 60)

    print("Last charge: {} to {}%".format(last_charge_timestamp, last_charge_value))
    print("Usage duration with screen turned on: {}h {}min".format(hours, minutes))


def get_pmset_log():
    raw_output = subprocess.check_output(["pmset", "-g", "log"])
    return str(raw_output, "utf-8") if sys.version_info.major >= 3 else raw_output


def get_last_charge_info(pmset_log):
    timestamp_raw, last_charge_value = re.findall(
        TIMESTAMP_REGEX + r"\s+\w+\s+.*Using AC \(Charge:(?P<charge>\d+)%\)", pmset_log
    )[-1]
    return convert_timestamp(timestamp_raw), last_charge_value


def get_time_with_display_turned_on(pmset_log, starting_from):
    all_times = re.findall(
        TIMESTAMP_REGEX + r"\s+\w+\s+Display is turned (?P<state>\w+)", pmset_log
    )
    display_times = [
        status
        for status in all_times
        if convert_timestamp(status[0])
        >= starting_from
    ]
    last_state_before_full_charge = all_times[-len(display_times) - 1]
    durations = []
    last_on = starting_from
    current_state = last_state_before_full_charge[-1]
    for entry in display_times:
        if entry[-1] == "on" and current_state == "off":
            last_on = convert_timestamp(entry[0])
        elif entry[-1] == "off" and current_state == "on":
            durations.append(
                (convert_timestamp(entry[0]) - last_on).total_seconds()
            )
        current_state = entry[-1]
    durations.append((datetime.now() - last_on).total_seconds())  # current usage
    return sum(durations)


def convert_timestamp(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    main()
    sys.exit(0)
