import sqlite3



con=sqlite3.connect("FFF1.db")
usertable=con.execute("CREATE TABLE 'users' ('ID'   INTEGER,'Name'	TEXT,'Username' TEXT,'Password'	TEXT,'Email'	TEXT,'Phone'	TEXT)")
con.commit()
usertable.close()

notetable=con.execute("CREATE TABLE 'notes' ('NoteID'	INTEGER,'OwnerID'	INTEGER,'Header'	TEXT,'Body'	TEXT)")
con.commit()
notetable.close()


con.close()
