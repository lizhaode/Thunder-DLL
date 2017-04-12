import py2exe
from distutils.core import setup

options = {"py2exe":{"compressed": 1,  
            "optimize": 2,  
            "bundle_files": 1 
            }}
setup(windows=[
    {
        "script":"main.py",
        "icon_resources":[(0, "downloader.ico")],
        "dest_base": "downloader"
    }
              ],
        options=options, 
        zipfile=None)