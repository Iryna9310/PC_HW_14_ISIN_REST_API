import json
from fastapi.testclient import TestClient
from main import app
from app.database import SessionLocal, engine
from app import models, crud

# Створення тестового клієнта за допомогою FastAPI додатку
client = TestClient(app)

# Перевизначення залежності бази даних для використання тестової бази даних
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[crud.get_db] = override_get_db


# Тести для маршруту /contacts
def test_create_contact():
    # Тест створення нового контакту
    new_contact = {
        "name": "John Doe",
        "surname": "Smith",
        "email": "john.smith@example.com",
        "phone": "1234567890",
        "birthday": "1990-01-01",
        "additional_info": "Some additional info"
    }
    response = client.post("/contacts/", json=new_contact)
    assert response.status_code == 200
    created_contact = response.json()
    assert created_contact["name"] == new_contact["name"]
    assert created_contact["email"] == new_contact["email"]


def test_get_contacts():
    # Тест отримання контактів
    response = client.get("/contacts/")
    assert response.status_code == 200
    contacts = response.json()
    assert len(contacts) > 0


def test_update_contact():
    # Тест оновлення існуючого контакту
    contact_id = 1  # Замінити на реальний ідентифікатор контакту з тестової бази даних
    updated_data = {
        "name": "Оновлене Ім'я",
        "phone": "9876543210"
    }
    response = client.put(f"/contacts/{contact_id}/", json=updated_data)
    assert response.status_code == 200
    updated_contact = response.json()
    assert updated_contact["name"] == updated_data["name"]
    assert updated_contact["phone"] == updated_data["phone"]


def test_delete_contact():
    # Тест видалення контакту
    contact_id = 1  # Замінити на реальний ідентифікатор контакту з тестової бази даних
    response = client.delete(f"/contacts/{contact_id}/")
    assert response.status_code == 200
    deleted_contact = response.json()
    assert deleted_contact["id"] == contact_id


 

