import pytest
from Main import app

def test_basic_get():
    
    response = app.test_client().get("/")
    
    assert response.status_code == 200
    
def test_basic_post():
    
    response = app.test_client().post("/create_user", json={
        "email":"user1@mail.ru",
        "password1":"1234567",
        "firstName":"name"
    })
    
    assert response.status_code == 200  
      
    response = app.test_client().post("/get_token", json={
        "email":"user1@mail.ru",
        "password":"1234567",
    })
    
    print("Сгенерированный JWT токен: ", response.json["access_token"] )
    assert response.status_code == 200
    
    saved_token = response.json["access_token"]

    response = app.test_client().post("/confirm_token", json={
        "access_token":str(saved_token),
    })
    
    print(response.json)
    
    assert response.status_code == 200  
    assert response.json["status"] == "correct"
    
def test_create_user_post():
    
    response = app.test_client().post("/", json={
        "login":"test_user",
        "password":"test_password",
    })
    
    assert response.status_code == 200
    
def test_request_token():
    
    response = app.test_client().post("/", json={
        "login":"test_user",
        "password":"test_password",
    })
    
    assert response.status_code == 200        
    

def test_validate_token():
    
    pass
    # assert response.status_code == 200   

def test_scenario():
    
    pass
    
    #assert response.status_code == 200   