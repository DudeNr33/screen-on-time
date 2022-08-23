# screen-on-time
A simple script to check how long you have actively used (e.g. display turned on) your MacBook since the last full charge.

## How to use
You can run this script without downloading it (thanks @hotrungnhan):
```shell
curl -s https://raw.githubusercontent.com/DudeNr33/screen-on-time/main/src/screen_on_time.py | python3 -s
```

Or just download the file ``src/screen_on_time.py``, make it executable via ``chmod +x screen_on_time.py`` and run it in your terminal: ``./screen_on_time.py``.
It is compatible with Python 3 and works without any additional dependencies. 
This means even if you are unfamilar with Python, you should be able to run it with just the instructions given above (assuming you know how to use a terminal).

## Disclaimer
The script relies on parsing the output of ``pmset -g log``.
This means that if those log messages change in the future or are different in the version of macOS you are running, the script will fail. 
Feel free to open an issue here on GitHub if you have problems.
Please attach the output of ``pmset -g log`` in to ease the analysis of the problem.
