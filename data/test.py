from sqlalchemy import text, create_engine
engine = create_engine('sqlite:///base_chapitre.db')
connection = engine.connect()
result = connection.execute(text("select name from items_C"))
for row in result:
    print(row)