# AnySecrets

**Effortless password management solution**

---

[![Test](https://github.com/everysoftware/anysecrets/actions/workflows/test.yml/badge.svg)](https://github.com/everysoftware/anysecrets/actions/workflows/test.yml)
[![CodeQL Advanced](https://github.com/everysoftware/anysecrets/actions/workflows/codeql.yml/badge.svg)](https://github.com/everysoftware/anysecrets/actions/workflows/codeql.yml)

---

## Features

* Create and manage passwords safely with an AES-256 encryption
* Search passwords easily by name or URL

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/everysoftware/anysecrets
    ```
2. Create `.env` file based on `.env.example`:

    ```bash
    cp .env.example .env
    ```

3. Run the application:

   ```bash
      make up
   ```

AnySecrets is available at [http://localhost:3014](http://localhost:3014):
![welcome.jpeg](assets/welcome.jpeg)

![main_page.jpeg](assets/main_page.jpeg)

Enjoy! 🚀

## API Reference

API docs are available at [http://localhost:8014/docs](http://localhost:8014/docs):

![api_reference.png](assets/api_reference.png)

## Tech Stack

---

**Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL, cryptography

**Frontend**: Python, FastAPI, Jinja2, HTML, CSS, JS

---

## Screenshots

![welcome.jpeg](assets/welcome.jpeg)
![login.jpeg](assets/login.jpeg)
![register.jpeg](assets/register.jpeg)
![main_page.jpeg](assets/main_page.jpeg)
![add_password.jpeg](assets/add_password.jpeg)
![password.jpeg](assets/password.jpeg)
![edit_password.jpeg](assets/edit_password.jpeg)
![profile.png](assets/profile.png)

**Made with ❤️**
