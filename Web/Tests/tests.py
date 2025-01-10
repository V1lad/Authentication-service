import pytest
from Main import app
from faker import Faker


def test_creating_and_confirming_jwt_for_user():
    
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
    
    assert response.status_code == 200
    
    saved_token = response.json["access_token"]

    response = app.test_client().post("/confirm_token", json={
        "access_token":str(saved_token),
    })
    
    print(response.json)
    
    assert response.status_code == 200  
    assert response.json["status"] == "correct"
    
def test_create_user_post():
    
    response = app.test_client().post("/create_user", json={
        "email":"test_user@mail.ru",
        "password1":"test_password",
        "firstName":"TESTTEST"
    })
    
    assert response.status_code == 200
    

def test_invalidate_token():
    
    response = app.test_client().post("/confirm_token", json={
        "access_token":str("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE3MzY1MTQxMzgsImV4cCI6MTczNjUxNTM0OSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.MhBZggor6cSnxqkbY1tw9mX3B_P2T-ArKxgV19zvuOQ"),
    })
    
    assert response.json["status"] == "Signature verification failed"
    assert response.status_code == 401


def test_scenario_with_other_service():
    
    fake = Faker()
    email = fake.ascii_email()
    # Создадим пользователя для тестового сценария
    response = app.test_client().post("/create_user", json={
        "email":email,
        "password1":email,
        "firstName": fake.name()
    })
    
    assert response.status_code == 200  
    
    # Сервис запрашивает JWT токен для пользователя
    response = app.test_client().post("/get_token", json={
        "email":email,
        "password":email,
    })
    
    assert response.status_code == 200  
    print("Сгенерированный JWT токен: ", response.json["access_token"] )
    
    saved_token = response.json["access_token"]
        
    # Через какое-то время другому сервису необходимо получить данные пользователя о разрешённых проектах. Для этого он сначала подтверждает JWT токен.
    response = app.test_client().post("/confirm_token", json={
        "access_token":str(saved_token)
    })
    
    assert response.json["status"] == "correct"
    assert response.status_code == 200  

    # В финальной части взаимодействия сервис управления проектами запрашивает информацию о пользователе с данным JWT токеном
    response = app.test_client().post("/get_rights", json={
        "access_token":str(saved_token)
    })
    
    assert response.json["permissions"] == '{}'
    assert response.status_code == 200  