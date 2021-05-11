# Script to extract WhatsApp chat and media for transfer from iPhone to Android

Reads Manifest.db from an iTunes backup of an iPhone and extracts the ChatStorage.sqlite and Media folder:

    ./output
  
        ChatStorage.sqlite
  
        Media/

These can then (hopefully) be transferred to an Android phone, and WhatsApp can be backed up using the WazzapMigrator app.

No idea how to get around paying for WazzapMigrator yet.

To run:
$ python3 extract.py
