'''
pip install keyboard
pip install mouse
pip install pyscreenshot
pip install pyautogui
pip install pypiwin32
'''
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

    def on_left_click(self):
        x, y = pag.position()
        self.x.append(x)
        self.y.append(y)

    def set_left_click_event(self):
        print('Press left-click twice to specity the capture range.')
        mouse.on_click(self.on_left_click)

    def unset_all_click_event(self):
        mouse.unhook_all()


def send_to_clipboard(data, clip_type=win32clipboard.CF_BITMAP): 
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data) 
    win32clipboard.CloseClipboard()

def save_screen_to_clipboard():
    '''
    Get a screenshot of the active application and save it to the clipboard.
    Capture range is specifed by mouse position.
    '''
    click = ClickEventHandler()
    click.set_left_click_event()
    while len(click.x) < 2:
        continue
    click.unset_all_click_event()

    im = ImageGrab.grab(bbox=(click.x[0], click.y[0], click.x[1], click.y[1]))
    im.save('temp.bmp', 'BMP')
    '''
    with io.BytesIO() as output:
        # Magic number '14' means bitmap header.
        im.convert("RGB").save(output, "BMP")
        im = output.getvalue()[14:]
    '''
    im = im.convert('RGB').tobytes()
    send_to_clipboard(im)
    print('Send the capture to clipboard')


if __name__ == '__main__':
    '''
    While this script being executed, you can save a screenshot of the active application to the clipboard.
    To do this, first press 'alt+s'. Then, press left-click twice. Capture range is specifed by mouse position.
    Windows OS only.

    Example:
    python screenshot.py

    Todo:
    Copying image to clipboard
    '''
    print('Press Ctrl-c to quit.')
    print('Press Alt-s to capture.')

    # Add hotkey. 'save_screen_to_clipboard' is executed after press 'alt+s'.
    keyboard.add_hotkey('alt+s', save_screen_to_clipboard, args=())

    # Block forever, like `while True`.
    keyboard.wait()
