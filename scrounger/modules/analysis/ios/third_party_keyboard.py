from scrounger.core.module import BaseModule

# helper functions
from scrounger.modules.misc.ios.local.app.symbols import Module as SymbolsModule
from scrounger.utils.config import Log
import re

class Module(BaseModule):
    meta = {
        "author": "RDC",
        "description": "Checks if an application checks of third party \
keyboards",
        "certainty": 65
    }

    options = [
        {
            "name": "binary",
            "description": "local path to the application's decrypted binary",
            "required": True,
            "default": None
        }
    ]

    _regex = r"UIApplicationKeyboardExtensionPointIdentifier"

    def run(self):
        result = {
            "title": "Application Does Not Check For Third-Party Keyboards",
            "details": "",
            "severity": "Medium",
            "report": False
        }

        symb_module = SymbolsModule()
        symb_module.binary = self.binary
        symbols_result, symbols = symb_module.run(), None
        for key in symbols_result:
            if key.endswith("_symbols"):
                symbols = symbols_result[key]

        if not symbols:
            return {"print": "Couldn't get symbols from binary."}

        Log.info("Analysing Symbols")
        if not re.search(self._regex, symbols):
            result.update({
                "report": True,
                "details": "No evidence of third party keyboard detection \
functions found."
            })

        return {
            "{}_result".format(self.name()): result
        }

