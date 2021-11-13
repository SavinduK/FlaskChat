from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from flask_login import current_user, login_required
from . import db
from .models import Chatroom,Message
views = Blueprint("views",__name__)
from flask_wtf.csrf import CSRFProtect

@views.route("/",methods=['GET','POST'])
@views.route("/home",methods=['GET','POST'])
def home():
    if request.method == "POST":
        chatroom = request.form.get("chatroom")
        username = request.form.get("username")
        if username and chatroom :
           chatroom_exists = Chatroom.query.filter_by(name=chatroom).first()
           if chatroom_exists:
               return redirect(f"/chatroom/{chatroom}/{username}")
               new
           else :
               new_chatroom = Chatroom(name=chatroom)
               db.session.add(new_chatroom)
               db.session.commit()
               return redirect(f"/chatroom/{chatroom}/{username}")
        else :
            flash("empty fields",category="error")
    return render_template("home.html")



@views.route("/chatroom/<chatroom>/<username>")
def chatroom(chatroom,username):
    messages = Message.query.filter_by(chatroom_name=chatroom)
    chatroom_data = Chatroom.query.filter_by(name=chatroom).first()
    msg_list =[]
    for message in messages :
       msg_list.append(message)
    curr_index =0
    if curr_index > 0 :
      curr_index = msg_list[len(msg_list)-1].id
    return render_template("chatroom.html",chatroom_data=chatroom_data,username=username,chatroom=chatroom,curr_index=curr_index)

@views.route("/send-message/<chatroom>/<username>",methods=['GET','POST'])
def post(chatroom,username):
    if request.method == "POST" :
        msg_request = request.get_json(force=True)
        message = msg_request['message']
        if message :
          new_message = Message(user_name=username,chatroom_name=chatroom,message=message)
          db.session.add(new_message)
          db.session.commit()
          
          return jsonify({ "success" :"message sent" } )
        return jsonify({"error" : "empty message"})

@views.route("get-json/<chatroom>/<username>",methods=['GET','POST'])
def json(chatroom,username):
    if request.method == "POST" :
        json_request = request.get_json(force=True)
        index = json_request['json_index']
        messages = Message.query.filter_by(chatroom_name=chatroom)
        msg_list = []
        json_messages = []
        json_usernames = []
        json_time = []
        for message in messages:
            if message.id > index :
                msg_list.append(message)
                json_messages.append(message.message)
                json_usernames.append(message.user_name)
                json_time.append(message.date_created)
        json_index = msg_list[len(msg_list)-1].id         
        if len(msg_list) > 0 :
           return jsonify({"index" : json_index, "messages" : json_messages, "usernames" : json_usernames, "time" : json_time})
        else :
            return jsonify({"error" : "error"},500)
