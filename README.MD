# FastAPI Project Documentation

This document explains how to use the FastAPI endpoints with examples demonstrating typical use cases for each endpoint using Thunder Client, a lightweight REST client extension for VS Code.

## Table of Contents

- [Authentication and User Management](#authentication-and-user-management)
  - [Register User](#register-user)
  - [Get Token (Login)](#get-token-login)
  - [Revoke Token (Logout)](#revoke-token-logout)
  - [Refresh Token](#refresh-token)
- [Secrets Management](#secrets-management)
  - [Submit Secret Information](#submit-secret-information)
  - [Retrieve Secret Details](#retrieve-secret-details)
- [File Handling and Processing](#file-handling-and-processing)
  - [Extract Text](#extract-text)
  - [Summarise Text](#summarise-text)
  - [Upload File](#upload-file)
  - [Download File](#download-file)

---

## Authentication and User Management

### Register User

**Endpoint:** `POST /register`  
**Description:** Registers a new user.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/register`.
3. In the `Body` tab, select `JSON` and add the request body:
   ```json
   {
     "username": "your_username",
     "password": "your_password",
     "email": "your_email@example.com"
   }
   ```
4. Click `Send`.

---

### Get Token (Login)

**Endpoint:** `POST /token`  
**Description:** Retrieves an OAuth2 access token by logging in with user credentials.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/token`.
3. In the `Body` tab, select `Form-Encoded` and add the following key-value pairs:
   - `username`: `johndoe`
   - `password`: `securepassword`
4. Click `Send`.

---

### Revoke Token (Logout)

**Endpoint:** `POST /revoke`  
**Description:** Revokes or logs out the user.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/revoke`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_token>`
4. Click `Send`.

---

### Refresh Token

**Endpoint:** `POST /refresh`  
**Description:** Refreshes an expired token.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/refresh`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_refresh_token>`
4. Click `Send`.

---

## Secrets Management

### Submit Secret Information

**Endpoint:** `POST /submit_secret`  
**Description:** Submits secret information for secure storage.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/submit_secret`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_token>`
4. In the `Body` tab, select `Form-Data` and add the following fields:
   - `saving_on_separate_remote_storage`: `true` (or another required value)
   - `file`: Upload a file (e.g., `example.txt`)
5. Click `Send`.

---

### Retrieve Secret Details

**Endpoint:** `GET /secret-details`  
**Description:** Retrieves stored secret details for the authenticated user.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `GET` and URL to `http://127.0.0.1:8000/secret-details`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_token>`
4. Click `Send`.

---

## File Handling and Processing

### Extract Text

**Endpoint:** `POST /extract`  
**Description:** Extracts text from a given file.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/extract?words=23`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_token>`
4. In the `Body` tab, select `Form-Data` and add:
   - `file`: Upload a file (e.g., `document.pdf`)
5. Click `Send`.

---

### Summarise Text

**Endpoint:** `POST /summarise`  
**Description:** Summarises extracted text.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/summarise?words=50&max_tokens=25&summary_counts=20`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_token>`
4. In the `Body` tab, select `Form-Data` and add:
   - `file`: Upload a file (e.g., `document.txt`)
5. Click `Send`.

---

### Upload File

**Endpoint:** `POST /upload`  
**Description:** Uploads a file and saves it locally or remotely.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `POST` and URL to `http://127.0.0.1:8000/upload?words=100&storage_directory_name=myStorage&category=example&max_tokens=25&summary_counts=25`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_token>`
4. In the `Body` tab, select `Form-Data` and add:
   - `file`: Upload a file (e.g., `upload_example.pdf`)
5. Click `Send`.

---

### Download File

**Endpoint:** `GET /download/{file_id}`  
**Description:** Downloads a file from the server or a remote location.

**Request Setup in Thunder Client:**

1. Create a new request.
2. Set the method to `GET` and URL to `http://127.0.0.1:8000/download/file123`.
3. In the `Headers` tab, add:
   - `Authorization`: `Bearer <your_token>`
4. Click `Send`.

---

> **Note:** Replace `<your_token>` with the actual token and `http://127.0.0.1:8000` with your server's address if different.
