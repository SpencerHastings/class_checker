from modules.class_check.checker import sqliteDiff, makeDB

# makeDB('20215', 'old.db')
# makeDB('20215', 'new.db')
results = sqliteDiff('old.db', 'new.db')

for result in results:
    print(result)
