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

