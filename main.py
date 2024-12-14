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
            print(user1)
            return render_template("index.html",PageName="MainPage",user=user1,isLogged=True)
        return render_template("index.html",PageName="MainPage",user="",isLogged=False)
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


if __name__=="__main__":
    app.run(port=5300)