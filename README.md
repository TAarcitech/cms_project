---

#### 🔐 3. **How authentication works**
Say something like:
> This project uses token-based authentication. After login, the user gets a token, which must be included in the headers (`Authorization: Token <your_token>`) of every protected API request.

---

#### 🧪 4. **How to test it using Postman**

Explain simple examples:

- **Register**: `/api/register/` (method: POST)
- **Login**: `/api/login/` (method: POST, returns token)
- **Create Content**: `/api/contents/` (method: POST, only for logged-in authors)
- **Admin Access**: Admin can GET, PATCH, DELETE all content.

---

#### ✅ 5. **How to run tests

Use the command below to run all tests and track coverage:

```bash
coverage run manage.py test

#### 💾 Save Coverage Report as Text File

To save the coverage summary as a `.txt` file (useful for submission or uploading), run:

```bash
coverage report > coverage_report.txt
