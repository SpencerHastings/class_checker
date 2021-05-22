from checker import makeDB, sqliteDiff

#makeDB('20211', 'old.db')
#makeDB('20211', 'new.db')
results = sqliteDiff('old.db', 'new.db')

for result in results:
    print(result)
