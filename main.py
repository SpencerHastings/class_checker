from checker import makeDB, sqliteDiff

makeDB('20211', 'old.db')
makeDB('20211', 'new.db')
#sqliteDiff('old.db', 'new.db')
