base url = http://127.0.0.1:8000/


POST http://127.0.0.1:8000/account/register/

BODY:{ 
    full_name
    email,
    phone
    role,
    password,
    confirm_password
}

POST http://127.0.0.1:8000/account/login/
BODY:
{
    email,password
}

POST http://127.0.0.1:8000/account/forgot_password/
BODY:{
    emial
}


POST  http://127.0.0.1:8000/account/reset_password/


BODY:{
    email,otp,new_password,confirm_password
}



GET,POST http://127.0.0.1:8000/posts/list/

BODY{
    content,image (optional)
}

GET,PUT,PATCH
http://127.0.0.1:8000/posts/list/4/


for like

POST http://127.0.0.1:8000/posts/list/1/like/


POST http://127.0.0.1:8000/posts/comment/
Body:{
    post,content
}
comment filter by post id 

http://127.0.0.1:8000/posts/comment/?post=2


GET,PUT,PATCH http://127.0.0.1:8000/posts/comment/4/



(for message)
POST http://127.0.0.1:8000/messages/
BODY :{
    receiver,
    message

}

PUT,PATCH,DELETE http://127.0.0.1:8000/messages/1/

(conversation get)

GET http://127.0.0.1:8000/messages/1/conversation/ 