# 📝 Django Content Management System (CMS) API

This is a backend-only Content Management System (CMS) built using Django REST Framework. It supports two roles: Admin and Author.

- Authors can register, log in, and manage their own content.
- Admins are seeded into the system and can manage all content.

---

## ⚙️ Tech Stack

- Python + Django + Django REST Framework
- SQLite (default DB)
- Token-based Authentication
- Test Coverage using coverage.py
- Follows Clean Code + TDD practices

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

### 2️⃣ Create and Activate Virtual Environment

python -m venv env
env\Scripts\activate       # On Windows
# OR
source env/bin/activate    # On Mac/Linux

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Run Migrations

python manage.py makemigrations
python manage.py migrate

### 5️⃣ Seed Admin User

python manage.py seed_admin

### 6️⃣ Run the Server

python manage.py runserver

---

## 🔐 Authentication

This project uses token-based authentication.

After login, include your token in the headers of every request to protected APIs like this:

Authorization: Token <your_token>

---

## 🧪 How to Test the API Using Postman

| Action               | Endpoint                | Method        | Auth Required |
|----------------------|-------------------------|---------------|----------------|
| Register Author      | /api/register/          | POST          | ❌ No          |
| Login                | /api/login/             | POST          | ❌ No          |
| Create Content       | /api/contents/          | POST          | ✅ Yes (Author) |
| View Own Content     | /api/contents/          | GET           | ✅ Yes (Author) |
| Update/Delete Own    | /api/contents/<id>/     | PATCH/DELETE  | ✅ Yes (Author) |
| Admin Manage Content | /api/contents/          | GET/PATCH/DELETE | ✅ Yes (Admin) |
| Search Content       | /api/contents/?search=keyword | GET     | ✅ Yes         |

---

## ✅ 5. How to Run Tests and View Coverage Report

Use the following commands to run all tests and track coverage:

coverage run manage.py test

---

### 💾 Save Coverage Report as Text File

To save the coverage summary as a .txt file (useful for submission or uploading), run:

coverage report > coverage_report.txt

This will create a file named `coverage_report.txt` in your project directory, containing a summary of your test coverage.

---

### 🌐 (Optional) View Coverage in Browser (HTML)

To generate and view a full visual report in your browser:

coverage html
start htmlcov\index.html    # On Windows
# or
open htmlcov/index.html     # On Mac/Linux

---

## 📁 Folder Structure

cms_project/
├── cms/                    # Main Django app
├── cms_project/            # Project settings
├── manage.py               # Entry point
├── requirements.txt        # Dependencies
├── htmlcov/                # Coverage HTML output (after running coverage)
├── coverage_report.txt     # Text summary of test coverage

---

## 📌 Notes

- Admin user is seeded using `python manage.py seed_admin`.
- Content access is role-based.
- Search works across title, body, summary, and category fields.
- Full TDD approach with field-level validations.

---

## 👤 Author

Developed as part of a Django assignment for API development using best practices.
