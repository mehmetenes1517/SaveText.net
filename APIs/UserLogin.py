from flask import Flask,request,jsonify,Response
from flask_cors import CORS
import sqlite3
import requests as rq

PORT=5101





app=Flask(__name__)
@app.route("/create",methods=["POST"])
def CreateUser():
    if(request.method=="POST"):
        user={
            "name":request.json["name"],
            "username":request.json["username"],
            "password":request.json["password"],
            "email":request.json["email"],
            "phone":request.json["phone"]
        }
        con=sqlite3.connect("FFF1.db")
        
        idcursor=con.execute("SELECT ID FROM users WHERE ID=(SELECT max(ID) FROM users)")

        id=idcursor.fetchall()[0][0]+1
        idcursor.close()


        checkcursor=con.execute("SELECT * FROM users WHERE username='{}' OR email='{}' OR phone='{}' ".format(user["username"],user["email"],user["phone"]))

        if(len(checkcursor.fetchmany())==0):
            checkuser={
                "name":request.json["name"],
                "username":request.json["username"],
                "password":request.json["password"],
                "email":request.json["email"],
                "phone":request.json["phone"]
            }
            cursor=con.execute("INSERT INTO users VALUES({},'{}','{}','{}','{}','{}');".format(id,user["name"],user["username"],user["password"],user["email"],user["phone"]))
            con.commit()

            cursor.close()
            checkcursor.close()
            
            con.close()
            return "ok",200
        else:
            checkcursor.close()
            con.close()
            return "user info already exist",500

    else:
        return 'Invalid Method Type',404

@app.route("/delete",methods=["DELETE"])
def DeleteUser():
    if(request.method=="DELETE"):
        con=sqlite3.connect("FFF1.db")
        cursor=con.execute("DELETE FROM users WHERE ID={}".format(request.json["id"]))
        con.commit()
        cursor.close()
        con.close()
        return "ok",200
    else:
        return 'Invalid Method Type',404


@app.route("/update",methods=["POST"])
def UpdateUser():
    if request.method=="POST":
        con=sqlite3.connect("FFF1.db")
        c=con.execute("SELECT * FROM users WHERE ID={}".format(request.json["id"]))
        if(len(c.fetchall())==0):
            return "this user does not exist",500

        cursor=con.execute("UPDATE users SET name='{}' ,username='{}', password='{}' ,email='{}', phone='{}' WHERE ID={}".format(request.json["name"],request.json["username"],request.json["password"],request.json["email"],request.json["phone"],request.json["id"]))
        con.commit()
        cursor.close()
        con.close()
        return"ok",200
@app.route("/get",methods=["POST"])
def GetUser():
    if(request.method=="POST"):
        con=sqlite3.connect("FFF1.db")
        cursor=con.execute("SELECT * FROM users WHERE ID={}".format(request.json["id"]))
        

        data=cursor.fetchone()
        id=data[0]
        name=data[1]
        username=data[2]
        password=data[3]
        email=data[4]
        phone=data[5]
        User={
            "id":id,
            "name":name,
            "username":username,
            "password":password,
            "email":email,
            "phone":phone
        }
        cursor.close()
        con.close()
        return User,200
    else:
        return "Invalid Method Type",404
    
@app.route("/check",methods=["POST"])
def CheckUser():
    if(request.method=="POST"):

        username=request.json["username"]
        password=request.json["password"]

        con=sqlite3.connect("FFF1.db")
        cursor=con.execute("SELECT password FROM users WHERE username='{}'".format(username))
        
        data=cursor.fetchone()
        if(len(data)==0):
            cursor.close()
            con.close()
            return "There is no user exists",404
        

        true_password=data[0]
        if(true_password==password):
            cursor.close()
            con.close()
            return "ok",200
        cursor.close()
        con.close()
        return "Password is not True" ,500
    else:
        return "Invalid Method Type",404


@app.route("/getID",methods=["POST"])
def GetUserID():
    if request.method=="POST":
        con=sqlite3.connect("FFF1.db")
        cursor=con.execute("SELECT ID FROM users WHERE username='{}'".format(request.json["username"]))
        data=cursor.fetchall()
        if(len(data)==0):
            return jsonify({"id":-1}),404
        id={
            "id":data[0][0]
        }
        return jsonify(id),200
    else:
        return "Invalid Method Type",404


@app.route("/register",methods=["POST"])
def RegisterUser():
    if request.method=="POST":
        con=sqlite3.connect("FFF1.db")
        user_cursor=con.execute("SELECT * FROM users WHERE username='{}' AND email='{}' ".format(request.json["username"],request.json["email"]))
        list1=user_cursor.fetchall()
        if(len(list1)==0):
            user_obj={
                "name":request.json["name"],
                "username":request.json["username"],
                "password":request.json["password"],
                "email":request.json["email"],
                "phone":request.json["phone"]
            }
            res=rq.post("http://127.0.0.1:{}/create".format(PORT),json=user_obj)
            res.close()
            if res.ok:
                user_cursor.close()
                con.close()
                return "ok",200
        user_cursor.close()
        con.close()
        return "user exist",500



if(__name__=="__main__"):
    app.run(port=PORT)
