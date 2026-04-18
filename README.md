# Profile Intelligence API

A Django REST API that enriches a name using external APIs and stores structured profile data.

---

## 🚀 Features

- External API integration:
  - Genderize
  - Agify
  - Nationalize

- Age group classification:
  - child
  - teenager
  - adult
  - senior

- Idempotent profile creation
- Filtering by gender, country, age group
- Full CRUD support

---

## 📡 Base URL (NGROK)


https://parturient-noncyclically-cody.ngrok-free.dev


---

## 📌 Endpoints

### Create Profile

POST /api/profiles


### Get All Profiles

GET /api/profiles


### Get Single Profile

GET /api/profiles/{id}


### Delete Profile

DELETE /api/profiles/{id}


---

## 🧪 Example Request

```json
{
  "name": "ella"
}
⚙️ Tech Stack
Django
Django REST Framework
SQLite/PostgreSQL
Requests
Ngrok
