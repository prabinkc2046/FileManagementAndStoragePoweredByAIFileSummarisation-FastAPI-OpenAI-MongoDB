# FastAPI Project Documentation

This document explains how to use the FastAPI endpoints. The examples demonstrate typical use cases for each endpoint and how to test them using **Thunder Client** in Visual Studio Code.

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

**Request Body (Form Data):**

- `username`: The username of the user (required)
- `password`: The password of the user (required)
- `email`: The email of the user (required)

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/register`.
3. Under the **Body** tab, select **Form**.
4. Add the following key-value pairs:
   - `username`: `your_username`
   - `password`: `your_password`
   - `email`: `your_email@example.com`

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/register" \
-H "Content-Type: application/json" \
-d '{"username": "johndoe", "password": "securepassword", "email": "johndoe@example.com"}'
```

### Get Token (Login)

**Endpoint:** `POST /token`  
**Description:** Retrieves an OAuth2 access token by logging in with user credentials.

**Form Data**:

- `username`: The user's username (required)
- `password`: The user's password (required)

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/token`.
3. Under the **Body** tab, select **Form**.
4. Add the following key-value pairs:
   - `username`: `your_username`
   - `password`: `your_password`

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/token" \
-d "username=johndoe&password=securepassword" \
-H "Content-Type: application/x-www-form-urlencoded"
```

### Revoke Token (Logout)

**Endpoint:** `POST /revoke`  
**Description:** Revokes or logs out the user.

**Headers**:

- `Authorization`: Bearer `<token>`

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/revoke`.
3. Under the **Headers** tab, add:
   - `Authorization`: `Bearer <your_token>`
4. No body is required.

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/revoke" \
-H "Authorization: Bearer <your_token>"
```

### Refresh Token

**Endpoint:** `POST /refresh`  
**Description:** Refreshes an expired token.

**Headers**:

- `Authorization`: Bearer `<token>`

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/refresh`.
3. Under the **Headers** tab, add:
   - `Authorization`: `Bearer <your_refresh_token>`
4. No body is required.

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/refresh" \
-H "Authorization: Bearer <your_refresh_token>"
```

---

## Secrets Management

### Submit Secret Information

**Endpoint:** `POST /submit_secret`  
**Description:** Submits secret information for secure storage.

**Form Data**:

- `open_api_key`: Optional string, API key.
- `remote_user`: Optional string, remote user.
- `remote_host`: Optional string, remote host.
- `ssh_password`: Optional string, SSH password.
- `password_key`: Optional string, password key.
- `saving_on_separate_remote_storage`: Boolean, whether to save on a separate remote storage (required).
- `file`: File upload.

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/submit_secret`.
3. Under the **Body** tab, select **Form**.
4. Add the following key-value pairs:
   - `open_api_key`: `your_api_key`
   - `remote_user`: `your_remote_user`
   - `remote_host`: `your_remote_host`
   - `ssh_password`: `your_ssh_password`
   - `password_key`: `your_password_key`
   - `saving_on_separate_remote_storage`: `true`
   - Attach a file to the `file` field.

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/submit_secret" \
-H "Authorization: Bearer <your_token>" \
-F "saving_on_separate_remote_storage=true" \
-F "file=@example.txt"
```

### Retrieve Secret Details

**Endpoint:** `GET /secret-details`  
**Description:** Retrieves stored secret details for the authenticated user.

**Headers**:

- `Authorization`: Bearer `<token>`

In **Thunder Client**:

1. Set the method to `GET`.
2. Set the URL to `http://127.0.0.1:8000/secret-details`.
3. Under the **Headers** tab, add:
   - `Authorization`: `Bearer <your_token>`
4. No body is required.

**Example Request**:

```bash
curl -X GET "http://127.0.0.1:8000/secret-details" \
-H "Authorization: Bearer <your_token>"
```

---

## File Handling and Processing

### Extract Text

**Endpoint:** `POST /extract`  
**Description:** Extracts text from a given file.

**Query Parameters**:

- `words`: Number of words to extract.

**Form Data**:

- `file`: File upload.

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/extract?words=23`.
3. Under the **Body** tab, select **Form** and upload the file.
4. Under the **Headers** tab, add:
   - `Authorization`: `Bearer <your_token>`

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/extract?words=23" \
-H "Authorization: Bearer <your_token>" \
-F "file=@document.pdf"
```

### Summarise Text

**Endpoint:** `POST /summarise`  
**Description:** Summarises extracted text.

**Query Parameters**:

- `words`: Number of words to consider.
- `max_tokens`: Maximum number of tokens to use.
- `summary_counts`: Number of words in the summary.

**Form Data**:

- `file`: File upload.

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/summarise?words=50&max_tokens=25&summary_counts=20`.
3. Under the **Body** tab, select **Form** and upload the file.
4. Under the **Headers** tab, add:
   - `Authorization`: `Bearer <your_token>`

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/summarise?words=50&max_tokens=25&summary_counts=20" \
-H "Authorization: Bearer <your_token>" \
-F "file=@document.txt"
```

### Upload File

**Endpoint:** `POST /upload`  
**Description:** Uploads a file and saves it locally or remotely.

**Query Parameters**:

- `words`, `category`, `max_tokens`, `summary_counts`, `storage_directory_name`.

**Form Data**:

- `file`: File upload.

In **Thunder Client**:

1. Set the method to `POST`.
2. Set the URL to `http://127.0.0.1:8000/upload?words=100&storage_directory_name=myStorage&category=example&max_tokens=25&summary_counts=25`.
3. Under the **Body** tab, select **Form** and upload the file.
4. Under the **Headers** tab, add:
   - `Authorization`: `Bearer <your_token>`

**Example Request**:

```bash
curl -X POST "http://127.0.0.1

:8000/upload?words=100&storage_directory_name=myStorage&category=example&max_tokens=25&summary_counts=25" \
-H "Authorization: Bearer <your_token>" \
-F "file=@myfile.txt"
```

### Download File

**Endpoint:** `GET /download`  
**Description:** Downloads the file previously uploaded.

**Query Parameters**:

- `file_id`: The ID of the file to download.

In **Thunder Client**:

1. Set the method to `GET`.
2. Set the URL to `http://127.0.0.1:8000/download?file_id=your_file_id`.
3. Under the **Headers** tab, add:
   - `Authorization`: `Bearer <your_token>`

**Example Request**:

```bash
curl -X GET "http://127.0.0.1:8000/download?file_id=your_file_id" \
-H "Authorization: Bearer <your_token>"
```
