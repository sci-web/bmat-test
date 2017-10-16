# bmat's test code
## data load and data access through web-interfaces

Directory structure:
```
csv:
    Input CSV data (modified, see section "Issues and odds" below)
dataload:
    Python code to load CSV data to mongodb
http:
    Flask stand-alone framework code
```

Mongodb version:
```
./bin/mongod --version
db version v3.4.7
```

Install:
```
from dataload dir run (mongodb server must be launched with default options):
python DataLoader.py
(drop mongo collections epg, music, channels if the above script is rerun)

```

MongoDB indexing after load:
```
Run in mongodb shell:
> db.epg.createIndex({"broadcast.program_local_title":'text',program_original_title:'text'})
```

DB structure:
```
Run in mongodb shell ():
> use bmat
> show collections
> db.epg.findOne()
> db.music.findOne()
> db.channels.findOne()

broadcast data appended to music collection on the data load stage (as they are statically linked) and
coincidence in channels music broadcasting 
(i.e. when the same music appears on different channels) is included in data structure
```

HTML Interfaces prerequisites:
```
Flask
To run:
python http/run.py

```

HTML Interfaces properties:
```
To see and try:
http://127.0.0.1:5000
Records by time period filtered on client side 
(also interfaces/code can be updated for clients to choose this period on their own)
```

Issues and odds:
```
1. comma separated CSV-s are bad if there are commas within fields 
    → CSVs are saved as tab separated
2. UTF-8 coding should be valid
    bson.errors.InvalidStringData: strings in documents must be valid UTF-8: 'Nuestra reina Pen\xe9lope'
    → encoded like str.decode('cp1252').encode('utf-8')
3. column names are to be standardized across different CSV-s
4. should not be new line symbols within the CSV cells
5. in epg.csv the original_title sometimes is empty, though can be recovered from local-original titles of other records 
    — did not correct this in the DB, but included local title column in Music​ ​tracking​ ​report​ interface
```