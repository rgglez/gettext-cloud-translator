"""
Gettext Cloud Translator

This Python script provides a tool for translating gettext .po files 
using OpenAI's GPT models or cloud services such as Microsoft Azure 
Translator. It is designed to handle both bulk and individual 
translation modes.

---

MIT License

Copyright (c) 2024 Rodolfo González

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import logging
import os
import time

import polib
from dotenv import load_dotenv

from gettext_cloud_translator.version import __version__

###############################################################################

class TranslationConfig:
    """ Class to hold configuration parameters for the translation service. """
    def __init__(self, args):
        self.model = args.model
        self.bulk_mode = args.bulk_mode
        self.fuzzy = args.fuzzy
        self.folder_language = args.folder_language
        self.source_language = args.source_language
        self.batch_size = 50
        self.total_batches = 0        
    # __init__
# TranslationConfig






















