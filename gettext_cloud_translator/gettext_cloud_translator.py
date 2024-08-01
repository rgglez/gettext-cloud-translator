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
import polib

from dotenv import load_dotenv
from version import __version__
from translator_factory import TranslatorFactory
from rich.pretty import pprint

###############################################################################

# Initialize environment variables and logging
load_dotenv()
logging.basicConfig(level=logging.INFO)

###############################################################################

class GettextCloudTranslator:
    def __init__(self, service) -> None:
        self.service = service
        self.config = service.config

        if self.config.fuzzy:
            self.disable_fuzzy_translations(self.config.file)        
    # __init__

    ###########################################################################

    def disable_fuzzy_translations(self):
        """
        Disables fuzzy translations in a .po file by removing the 'fuzzy' flags from entries.
        """
        try:
            po_file = polib.pofile(self.config.file)

            fuzzy_entries = [entry for entry in po_file if 'fuzzy' in entry.flags]
            for entry in fuzzy_entries:
                entry.flags.remove('fuzzy')

            self.po_file.save(self.config.file)
            logging.info("Fuzzy translations disabled in file: %s", self.config.file)
        except Exception as e:  # pylint: disable=W0718
            logging.error("Error while disabling fuzzy translations in file %s: %s", self.config.filepo_file_path, e)    
    # disable_fuzzy_translations    

    ###########################################################################

    def update_po_entry(self, original_text, translated_text, po_file):
        """Updates a .po file entry with the translated text."""
        entry = po_file.find(original_text)
        if entry:
            logging.info("Applying to %s", entry.msgid)
            entry.msgstr = translated_text
    # update_po_entry 

    ###########################################################################

    def apply_translations_to_po_file(self, translated_texts, po_file):
        """
        Applies the translated texts to the .po file.
        """

        for translation in translated_texts:
            if translation["msgstr"]:
                self.update_po_entry(translation["msgid"], translation["msgstr"], po_file)
            else:
                logging.warning("No original text found for index %s", translation["msgid"])
    # apply_translations_to_po_file
  
    ###########################################################################

    def process_translations(self, texts_to_translate):
        """Processes translations either in bulk or one by one."""
        if self.config.bulk:          
            return self.service.translate_in_bulk(texts_to_translate)
        else:
            return self.service.translate_one_by_one(texts_to_translate)
    # process_translations    

    ###########################################################################    

    def translate(self):
        try:            
            po_file = polib.pofile(self.config.file)
            file_lang = po_file.metadata.get('Language', '')
            
            if file_lang[:2] != self.config.dstlang:
                logging.warning("Skipping .po file due to inferred language mismatch: %s", self.config.file)
                return

            texts_to_translate = [
                entry.msgid
                for entry in po_file
                if not entry.msgstr and entry.msgid and 'fuzzy' not in entry.flags
            ]
            
            translated_texts = self.process_translations(texts_to_translate)

            logging.info("Applying %i translations to %s", len(translated_texts), self.config.file)
            self.apply_translations_to_po_file(translated_texts, po_file)

            po_file.save()

            logging.info("Finished processing .po file: %s", self.config.file)
        except Exception as e:  # pylint: disable=W0718
            logging.error("Error processing file %s: %s", self.config.file, e)    
    # process_po_file
# GettextCloudTranslator

###############################################################################

def main():
    """Main function to parse arguments and initiate processing."""
    parser = argparse.ArgumentParser(description="Scan and process .po files")
    parser.add_argument("--version", action="version", version=f'%(prog)s {__version__}')
    parser.add_argument("--backend", required=True, default="azure", choices=["chatgpt", "azure"])
    parser.add_argument("--apikey", help="Service API key")
    parser.add_argument("--model", default="gpt-3.5-turbo-1106", help="OpenAI model to use for translations, for the ChatGPT backend.")
    parser.add_argument("--location", help="Microsoft Azure location")
    parser.add_argument("--file", required=True, help="Input .po file")
    parser.add_argument("--srclang", required=False, choices=["en", "es"], default="en", help="The ISO code for the language of the source strings. Defaults to 'en' (English)")
    parser.add_argument("--dstlang", required=False, help="The ISO code for the language to translate to")
    parser.add_argument("--fuzzy", action="store_true", help="Remove fuzzy entries")
    parser.add_argument("--bulk", action="store_true", help="Use bulk translation mode")
    parser.add_argument("--bulksize", default=49500, type=int, help="Batch size for bulk translation")        

    args = parser.parse_args()
    args.apikey = args.apikey if args.apikey else os.getenv("API_KEY")

    translator = GettextCloudTranslator(TranslatorFactory().create_translator(args))
    translator.translate()
# main

###############################################################################

if __name__ == "__main__":
    main()
# __main__