# Secrets Backend

![GitHub](https://img.shields.io/github/license/everysoftware/secrets)

Simple self-hosted password manager.

---

**Backend:** https://github.com/everysoftware/secrets-backend

**Frontend:** https://github.com/everysoftware/secrets-frontend

---

## Features

* **Secure authentication**. JWT-based authentication with access tokens.
* **Password encryption**. Passwords are encrypted with AES-256.

## Stack

Python 3.12 • FastAPI • SQLAlchemy • cryptography

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/everysoftware/secrets-backend
    ```
2. Create `.env` based on `.env.example`.

3. Start the application:

    ```bash
       make up
    ```

## API Reference

![img.png](assets/api_reference.png)
