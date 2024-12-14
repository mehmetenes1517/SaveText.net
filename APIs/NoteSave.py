from flask import request,Flask
import sqlite3
app=Flask(__name__)

@app.route("/add",methods=["POST"])
def AddNote():
    if(request.method=="POST"):
        con=sqlite3.connect("FFF1.db")
        
        idcheck=con.execute("SELECT * FROM notes WHERE NoteID=(SELECT max(NoteID) FROM notes)")
        tuple_id=idcheck.fetchall()
        if(len(tuple_id)==0):
            id=0
        else:
            id=tuple_id[0][0]+1
        print(id)
        idcheck.close()

        addNote=con.execute("INSERT INTO notes VALUES({},{},'{}','{}')".format(id,request.json["OwnerID"],request.json["header"],request.json["body"]))
        con.commit()
        

        addNote.close()
        con.close()



        return "ok",200
    else:
        return "Invalid Method Type",404
@app.route("/update",methods=["POST"])
def UpdateNote():
    if request.method=="POST":
        con=sqlite3.connect("FFF1.db")

        updatecursor=con.execute("UPDATE notes SET header='{}',body='{}' WHERE NoteID={}".format(request.json["header"],request.json["body"],request.json["NoteID"]))
        con.commit()

        updatecursor.close()
        con.close()


        return "ok",200
    else:
        return "Invalid Method Type",404
@app.route("/delete",methods=["POST"])
def DeleteNote():
    if request.method=="POST":
        con=sqlite3.connect("FFF1.db")
        deleted=con.execute("DELETE FROM notes WHERE NoteID={} AND OwnerID={}".format(request.json["NoteID"],request.json["OwnerID"]))
        con.commit()



        deleted.close()
        con.close()
        return "ok",200
    else:
        return "Invalid Method Type",404

@app.route("/getnotes",methods=["POST"])
def GetNotes():
    if request.method=="POST":
        con=sqlite3.connect("FFF1.db")
        note_cursor=con.execute("SELECT * FROM notes WHERE OwnerID={}".format(request.json["OwnerID"]))
        note_list=note_cursor.fetchall()
        note_cursor.close()
        con.close()
        return note_list,200
    else:
        return "Invalid Method Type",404
@app.route("/getnote",methods=["GET"])
def GetNote():
    if request.method=="GET":
        con=sqlite3.connect("FFF1.db")
        note_cursor=con.execute("SELECT * FROM notes WHERE NoteID={}".format(request.json["NoteID"]))
        note=note_cursor.fetchall()
        if(len(note)==0):
            return "there is no note exists",500
        note_obj={
            "NoteID":note[0][0],
            "OwnerID":note[0][1],
            "header":note[0][2],
            "body":note[0][3]
        }

        return note_obj,200

    else:
        return "Invalid Method Type",404

if __name__=="__main__":
    app.run(port=5102)