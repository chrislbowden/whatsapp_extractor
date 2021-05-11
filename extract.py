import os
import shutil
import sqlite3

BASE_DIR = "/Users/chris.bowden/Library/Application Support/MobileSync/Backup/"
BACKUP = "d0147a0e0d8b224ab90adcf99511bf983cbcaac2/"
OUTPUT_DIR = "./output/"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# sqlite db describing file structure of backup
MANIFEST = BASE_DIR + BACKUP + "Manifest.db"

# Chat storage is always in the same place
CHAT_STORAGE = BASE_DIR + BACKUP + "7c/7c7fba66680ef796b916b067077cc246adacf01d"
CHAT_STORAGE_DEST = OUTPUT_DIR + "ChatStorage.sqlite"
EXTS_TO_COPY = {'docx', 'jpg', 'mp3', 'mp4', 'opus', 'pdf', 'thumb','webp'}

"""
Structure of Manifest.db:
$ sqlite3 Manifest.db
sqlite> .schema Files
CREATE TABLE Files (fileID TEXT PRIMARY KEY, domain TEXT, relativePath TEXT, flags INTEGER, file BLOB);
CREATE INDEX FilesDomainIdx ON Files(domain);
CREATE INDEX FilesRelativePathIdx ON Files(relativePath);
CREATE INDEX FilesFlagsIdx ON Files(flags);
"""
media_files_query = (
	"SELECT fileID, relativePath "
	"FROM Files "
	"WHERE domain LIKE '%WhatsApp%' "
	"AND relativePath LIKE '%Message/Media%'"
)

# Fetch the list of media files from Manifest.db
con = sqlite3.connect(MANIFEST)
cur = con.cursor()
cur.execute(media_files_query)
results = cur.fetchall()
con.close()

new_paths = {}

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


shutil.copyfile(CHAT_STORAGE, CHAT_STORAGE_DEST)

for fileID, relativePath in results:
	try:
		# Manifest also lists the directories, we'll create there on the fly
		# from the file names so exclude these
		if relativePath.split(".")[-1] in EXTS_TO_COPY:
			new_paths[fileID] = OUTPUT_DIR + relativePath.split("Message/")[1]

	except IndexError:
		print(f"Error: {fileID}, {relativePath}")


for fileID, relativePath in new_paths.items():
	loc = find(fileID, BASE_DIR)
	os.makedirs(os.path.dirname(relativePath), exist_ok=True)
	shutil.copy(loc, relativePath)
	print(f"Copied {loc} to {relativePath}")
