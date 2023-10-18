# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
qrcodescreen.py

Implements an inherited kivy.uix.screenmanager.Screen
for display QRCodes    
"""

##################
# Standard library
##################
from threading import Thread

#######################
# Third party libraries
#######################
from functools import partial
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L

################
# Kivy libraries
################
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image

# pylint: disable=no-name-in-module
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    ObjectProperty,
)

#################
# Local libraries
#################
from utils.log import logger


class QRCodeScreen(Screen):
    """
    Class responsible to display qrcodes.

    It's an custom clone from
    https://pypi.org/project/kivy-garden.qrcode/
    and
    https://github.com/odudex/krux/blob/android/android/mocks/lcd_mock.py
    """

    code = StringProperty("")
    """
    The string code to be parsed on QRCode.        
    """

    text = StringProperty("")
    """
    The label to be show describing the QRCode
    """

    version = NumericProperty(1)
    """
    The QRCode version. GO from 1 to 40.
    """

    ecc = NumericProperty(ERROR_CORRECT_L)
    """
    The error correction code level for the qrcode.

    :data:`ecc` is the Error Correrction Code level.
    The default value is a constant in :module:`~qrcode.constants`,
    defaulting to `qrcode.constants.ERROR_CORRECT_L`.
    """

    box_size = 10
    """
    Size of box
    """

    border_size = 3
    """
    Size of border
    """

    background_color = ListProperty((0, 0, 0, 1))
    """
    :data:`fill_color` is a tuple describing the color of filled dots
    defined at :class:`~qrcode.QRCode`
    """

    fill_color = ListProperty((1, 1, 1, 1))
    """
    :data:`background_color` is a tuple describing the color of background
    defined at :class:`~qrcode.QRCode`
    """

    loading_image = StringProperty("data/images/image-loading.gif")
    """
    Intermediate image to be displayed while the widget ios being loaded.

    :data:`loading_image` is a :class:`~kivy.properties.StringProperty`,
    defaulting to `'data/images/image-loading.gif'`.
    """

    image_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 0.5})
    """
    :data:`ìmage_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """

    label_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 0.125})
    """
    :data:`label_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """

    warn_pos_hint = ObjectProperty({"center_x": 0.5, "center_y": 0.9})
    """
    :data:`warn_pos_hint` is a :class:`~kivy.properties.ObjectProperty`, 
    to set the default position on Screen
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._label_warn = None
        self._label_desc = None
        self._qrcode = None
        self._qrtexture = None
        self._img = None
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        if self._keyboard.widget:
            logger("WARNING", "QRCodeScreen: This widget is a VKeyboard object")
            # which you can use
            # to change the keyboard layout.
            passss
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_pre_enter(self, *args):
        """
        Event fired when the screen is about to be used: the entering animation is started.
        """
        self.set_label_warn()
        self.set_label_desc()
        self.set_image()
        Thread(target=partial(self.generate_qrcode)).start()

    def on_touch_down(self, touch):
        """
        Event fired when user clicked and release the left mouse button
        (or the touchable screen)
        """
        self._back_to_signscreen()

    def set_image(self):
        """
        Sets and add Image Widget to QRCodeScreen
        """
        self._img = Image(
            pos_hint=self.image_pos_hint,
            allow_stretch=True,
            size_hint=(None, None),
            size=(Window.height * 0.60, Window.height * 0.6),
        )

        self.add_widget(self._img)
        logger("INFO", "QRCodeScreen: <Image> added")

    def set_label_warn(self):
        """
        Sets and add Label Widget that warn user about
        the what to do on QRCodeScreen
        """
        self._label_warn = Label(
            text="\n".join(
                [
                    "[b]To sign this file with Krux:[/b]",
                    "",
                    " (a) load a 12/24 words key, with or without BIP39 password;",
                    " (b) use the Sign -> Message feature;",
                    " (c) scan this QR code below;",
                    " (d) click on screen or type one of 'esc|backspace|enter|left' keys to proceed.",
                ]
            ),
            font_size=Window.height // 35,
            font_name="terminus.ttf",
            halign="center",
            color=self.fill_color,
            markup=True,
            pos_hint=self.warn_pos_hint,
        )
        self.add_widget(self._label_warn)
        logger("INFO", "QRCodeScreen: <Label::warning> added")

    def set_label_desc(self):
        """
        Sets and add Label Widget that describe the qrcode's
        data to QRCodeScreen
        """
        self._label_desc = Label(
            text=self.text,
            font_size=Window.height // 35,
            font_name="terminus.ttf",
            halign="center",
            color=self.fill_color,
            markup=True,
            pos_hint=self.label_pos_hint,
        )
        self.add_widget(self._label_desc)
        logger("INFO", "QRCodeScreen: <Label::description> added")

    def generate_qrcode(self):
        """
        Setup QRCode
        """
        logger("INFO", "QRCodeScreen: Creating")
        self._qrcode = QRCode(
            version=self.version,
            error_correction=self.ecc,
            box_size=self.box_size,
            border=self.border_size,
        )
        self._qrcode.add_data(self.code)
        logger("DEBUG", "QRCodeScreen: data added")

        self._qrcode.make(fit=True)
        self._update_texture()

    def _create_texture(self, k, dt):
        logger("DEBUG", "QRCodeScreen: <Texture> creating")
        self._qrtexture = Texture.create(size=(k, k), colorfmt="rgb")
        # don't interpolate texture
        self._qrtexture.min_filter = "nearest"
        self._qrtexture.mag_filter = "nearest"

    def _update_texture(self):
        matrix = self._qrcode.get_matrix()
        k = len(matrix)
        logger("DEBUG", f"QRCodeScreen: <Texture::matrix::len>={k}")

        # create the texture in main UI thread otherwise
        # this will lead to memory corruption
        logger("DEBUG", "QRCodeScreen: <Texture> in mainUI Thread")
        Clock.schedule_once(partial(self._create_texture, k), -1)

        _color = self.fill_color[:]
        color = (int(_color[0] * 255), int(_color[1] * 255), int(_color[2] * 255))

        # used bytearray for python 3.5 eliminates need for btext
        buff = bytearray()
        for row in range(k):
            for col in range(k):
                buff.extend([0, 0, 0] if matrix[row][col] else color)

        # then blit the buffer
        # join not necessary when using a byte array
        # buff =''.join(map(chr, buff))
        # update texture in UI thread.
        logger("DEBUG", "QRCodeScreen: Blitting buffer in <QRCodeScreen@Texture>")
        Clock.schedule_once(lambda dt: self._upd_texture(buff))

    def _upd_texture(self, buff):
        texture = self._qrtexture

        if not texture:
            logger("WARNING", "QRCodeScreen: Texture hasn't been created")
            Clock.schedule_once(lambda dt: self._upd_texture(buff))
            return

        texture.blit_buffer(buff, colorfmt="rgb", bufferfmt="ubyte")
        texture.flip_vertical()
        self._img.anim_delay = -1
        self._img.texture = texture
        self._img.canvas.ask_update()
        logger("DEBUG", "QRCodeScreen: <Texture> updated")

    def _back_to_signscreen(self):
        """
        Back to SignScreen
        """
        logger("DEBUG", "QRCodeScreen: Redirecting to <SignScreen>")
        self.manager.transition.direction = "right"
        self.manager.current = "sign"

    def _keyboard_closed(self):
        logger("WARNING", "QRCodeScreen: keyboard have been closed")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == "escape":
            self._back_to_signscreen()

        elif keycode[1] == "enter":
            self._back_to_signscreen()

        elif keycode[1] == "left":
            self._back_to_signscreen()

        elif keycode[1] == "backspace":
            self._back_to_signscreen()
        else:
            logger("WARNING", f"QRCodeScreen: key '{keycode[1]}' not implemented")

        return True