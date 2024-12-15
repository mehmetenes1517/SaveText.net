from flask_cors import CORS
from flask import Flask,render_template,session,request,redirect,url_for
import requests as rq
import sqlite3


def getUser(id):
    response=rq.post("http://127.0.0.1:5101/get",json={"id":id})
    if(response.status_code==200):
        user={
            "id":id,
            "name":response.json()["name"],
            "username":response.json()["username"],
            "password":response.json()["password"],
            "email":response.json()["email"],
            "phone":response.json()["phone"]
        }
        return user

def getNote(id):
    response=rq.get("http://127.0.0.1:5102/getnote",json={"NoteID":id})
    if response.status_code==200:
        note={
            "NoteID":id,
            "OwnerID":response.json()["OwnerID"],
            "header":response.json()["header"],
            "body":response.json()["body"]
        }
        return note
    else:
        return {"NoteID":0,
            "OwnerID":0,
            "header":0,
            "body":0}

def getName(id):
    response=rq.post("http://127.0.0.1:5101/get",json={"id":id})
    if(response.status_code==200):
        return response.json()["name"]

database=sqlite3.connect("FFF1.db")

app=Flask(__name__)
app.secret_key="a"
author={
    "name":"Mehmet Enes Gedikoğlu",
    "email":"mehmetenesgedikoglu@gmail.com"
}



#MAİN PAGE


@app.route("/",methods=["GET","POST"])
@app.route("/main",methods=["GET","POST"])
@app.route("/index",methods=["GET","POST"])
def main():
    if(request.method=="GET"):
        if "userID" in session:
            # if session is opened
            user1=getUser(session["userID"])

            res=rq.post("http://127.0.0.1:5102/getnotes",json={"OwnerID":session["userID"]})
            notes=res.json()
                
            return render_template("index.html",notes=notes,user=user1,PageName="MainPage",isLogged=True)
        return render_template("index.html",notes=[],user="",PageName="MainPage",isLogged=False)
    elif (request.method=="POST"):
        return redirect(url_for("main"))





#ABOUT US SECTION
@app.route("/about")
def about():
    if "userID" in session:
        return render_template("about.html",PageName="About Us",user=getUser(session["userID"]),author=author,isLogged=True)
         
    return render_template("about.html",PageName="About Us",user="",author=author,isLogged=False)






#LOGOUT PAGE
@app.route("/logout",methods=["GET"])
def LogOut():
    session.clear()
    return redirect(url_for("main"))

#LOGIN
@app.route("/login",methods=["GET","POST"])
def Login():
    if request.method=="POST":
        object1={
            "username":request.form["username"],
            "password":request.form["password"]
        }

        response=rq.post("http://127.0.0.1:5101/check",json=object1)
        #print("x")
        if(response.ok==True):
            idobj={
                "username":request.form["username"]
            }
            
            r=rq.post("http://127.0.0.1:5101/getID",json=idobj)
            if(r.status_code==200):
                print("aaaaa")
                session["userID"]=r.json()["id"]

                r.close()
                return redirect(url_for("main"))
            

            response.close() 
        return redirect(url_for("Login"))
    elif request.method=="GET":
        return render_template("Login.html",PageName="Login",isLogged=False)
   
@app.route("/info",methods=["GET","POST"])
def UserInfo():
    if(request.method=="GET"):
        if "userID" in session:
            return render_template("UserInfo.html",user=getUser(session["userID"]),PageName="User Information",isLogged=True)
        else:
            return render_template("UserInfo.html",user="",PageName="User Information",isLogged=False)
    elif request.method=="POST":

        updated_user={
            "id":request.form["id"],
            "name":request.form["name"],
            "username":request.form["username"],
            "password":request.form["password"],
            "email":request.form["email"],
            "phone":request.form["phone"]
        }


        response=rq.post("http://127.0.0.1:5101/update",json=updated_user)            

        return redirect(url_for("UserInfo"))


@app.route("/notes/<int:index>",methods=["GET","POST"])
def Notes(index):
    if request.method=="GET":
        if "userID" in session:
            id_obj={
                "NoteID":index
            }
            res=rq.get("http://127.0.0.1:5102/getnote",json=id_obj)
            return render_template("notepage.html",note=res.json(),user=getUser(session["userID"]),PageName=f"NoteID {index}",isLogged=True)
    elif request.method=="POST":
        if "userID" in session:
            delete_json={
                "NoteID":index,
                "OwnerID":session["userID"]
            }
            response=rq.post("http://127.0.0.1:5102/delete",json=delete_json)         
            if(response.ok==True):
                return redirect(url_for("main"))
    else:
        return "Not Found",404

@app.route("/addnote",methods=["GET","POST"])
def AddNote():
    if request.method =="GET":
        if "userID" in session:
            return render_template("AddNote.html",isLogged=True,PageName="Add Note",user=getUser(session["userID"]))
        else:
            return render_template("AddNote.html",isLogged=False,PageName="",user={})
    elif request.method=="POST":
        if "userID" in session:
            noteobj={
                "OwnerID":session["userID"],
                "header":request.form["header"],
                "body":request.form["body"]
            }
            response=rq.post("http://127.0.0.1:5102/add",json=noteobj)
            return redirect(url_for("main"))

@app.route("/update/<int:index>",methods=["GET","POST"])
def UpdateNote(index):
    if request.method=="POST":
        note_obj={
            "NoteID":index,
            "header":request.form["header"],
            "body":request.form["body"]
        }
        response=rq.post("http://127.0.0.1:5102/update",json=note_obj)
        return redirect(url_for("main"))
    elif request.method=="GET":
        if "userID" in session:
            return render_template("UpdateNote.html",note=getNote(index),isLogged=True,PageName="Update Note",user=getUser(session["userID"]))
        else:
            return render_template("UpdateNote.html",note={},isLogged=False,PageName="",user={})



@app.route("/registeruser",methods=["GET","POST"])
def RegisterUser():
    if request.method=="POST":
        user_obj={
                "name":request.form["name"],
                "username":request.form["username"],
                "password":request.form["password"],
                "email":request.form["email"],
                "phone":request.form["phone"]
            }
        res=rq.post("http://127.0.0.1:5101/register",json=user_obj)
        if res.ok:
            return redirect(url_for("main"))
        else:
            return redirect(url_for("registeruser"))
    elif request.method=="GET":
        if "userID" in session:
            return render_template("Register.html",isLogged=True,PageName="Register",user=getUser(session["userID"]))
        else:
            return render_template("Register.html",isLogged=False,PageName="Register",user={})



if __name__=="__main__":
    app.run(port=5300)