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
filechooser.py

implements a inherited class of FileChooserIconView    
"""
####################
# Standard libraries
####################
import os

########################
# Thirdy party libraries
########################
from kivy.uix.filechooser import FileChooserListView

# @see stackoverflow.complex/questions/65547279/
#      /no-name-object-property-in-module-kivy-properties
#      -pylint-no-name-in-module
# pylint: disable=no-name-in-module
from kivy.properties import ObjectProperty, BooleanProperty


class LoadDialog(FileChooserListView):
    """
    FileChooser

    Class to manage the file to choose in SignScreen and VerifyScreen
    classes. In SignScreen, it will choose the file to load a content,
    write it in a .sha256.txt file and show qrcode content.
    """

    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    dirseclect = BooleanProperty(True)
    path = os.path.expanduser("~")
