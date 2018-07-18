'''
pip install keyboard
pip install mouse
pip install pyscreenshot
pip install pyautogui
pip install pypiwin32
'''
from PIL import Image
import io
import keyboard
import mouse
import pyscreenshot as ImageGrab
import pyautogui as pag
import win32clipboard

class ClickEventHandler(object):
    def __init__(self):
        self.x = []
        self.y = []

    def on_right_click(self):
        x, y = pag.position()
        self.x.append(x)
        self.y.append(y)

    def set_right_click_event(self):
        mouse.on_button(self.on_right_click, buttons='right', types='down')
        mouse.on_button(self.on_right_click, buttons='right', types='up')

    def unset_all_click_event(self):
        mouse.unhook_all()

def specify_range():
    click = ClickEventHandler()
    click.set_right_click_event()
    print('Drag mouse by right-click to specity the capture range')
    while len(click.x) < 2:
        continue
    click.unset_all_click_event()
    return click.x[0], click.y[0], click.x[1], click.y[1]

def send_to_clipboard(data, clip_type=win32clipboard.CF_DIB): 
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data) 
    win32clipboard.CloseClipboard()

def transform_pil_to_bmp(im):
    output = io.BytesIO()
    im.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    return data

def save_screen_to_clipboard():
    '''
    Get a screenshot of the active application and save it to the clipboard.
    Capture range is specifed by mouse drag.
    '''
    x0, y0, x1, y1 = specify_range()
    im = ImageGrab.grab(bbox=(x0, y0, x1, y1))
    # save to temporary file
    im.save('temp.bmp', 'BMP')

    # send image to clipboard
    data = transform_pil_to_bmp(im)
    send_to_clipboard(data)
    print('Send the capture to clipboard')


if __name__ == '__main__':
    '''
    While this script being executed, you can save a screenshot of the active application to the clipboard.
    To do this, first press 'alt+s'. Then drag mouse by right-click to specify the capture range.
    Windows OS only.

    Example:
    python screenshot.py
    '''
    print('Press Ctrl-c to quit.')
    print('Press Alt-s to capture.')

    # Add hotkey. 'save_screen_to_clipboard' is executed after press 'alt+s'.
    keyboard.add_hotkey('alt+s', save_screen_to_clipboard, args=())

    # Block forever
    keyboard.wait()
