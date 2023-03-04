import colorama
import json
from typing import Union, List, Dict

colorama.init()

_get_color_from_str = lambda clr : {
    'error': colorama.Fore.RED,
    'warning': colorama.Fore.YELLOW,
    'info': colorama.Fore.GREEN,
    'debug': colorama.Fore.BLUE,
    'red': colorama.Fore.RED,
    'green': colorama.Fore.GREEN,
    'yellow': colorama.Fore.YELLOW,
    'blue': colorama.Fore.BLUE,
    'magenta': colorama.Fore.MAGENTA,
    'cyan': colorama.Fore.CYAN,
    'white': colorama.Fore.WHITE,
}.get(clr.lower(), colorama.Fore.WHITE)

def c_print(*msg, **kwargs):
    color = _get_color_from_str(kwargs.get('color', None))
    end = kwargs.get('end', '\n')
    if color:
        print(color , msg , colorama.Style.RESET_ALL, end=end)
    else:
        print(msg)


def print_json(data: Union[Dict, List]) -> None:
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    c_print('hello', color='red')
    c_print('hello', color='green')
    c_print('hello', color='yellow')
    c_print('hello', color='blue')
    c_print('hello', color='magenta')
    c_print('hello', color='cyan')
    c_print('hello', color='white')
    c_print('hello', color='error')
    c_print('hello', color='warning')
    c_print('hello', color='info')
    c_print('hello', color='debug')