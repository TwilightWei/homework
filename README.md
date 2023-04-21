# Requirements
- Docker

# Deployment Process
1. cd to project root directory.
2. Pull images "docker compose pull"
3. Run db container "docker compose up -d db"
4. Connect to mysql db with the following credential.
    - Host: localhost
    - Username: root
    - Password: root
    - Port: 8080
5. Initialize the database with the following scripts.
    ```
    CREATE DATABASE homework;
    USE homework;

    CREATE TABLE `customer`(
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `username` VARCHAR(32) UNIQUE,
        `password` VARCHAR(64),
        `password_iv` VARCHAR(24),
        `password_ver_count` TINYINT NOT NULL DEFAULT 0,
        `password_ver_at` DATETIME NOT NULL,
        `updated_at` DATETIME NOT NULL,
        `created_at` DATETIME NOT NULL
    );
    ```
6. Run flask and nginx container "docker compose up -d flask nginx"

# APIs
- Create account
    - URL: http://localhost:8000/account/create
    - Method Type: POST
    - Payload:
        ```
        {
            "username": "myusername",
            "password": "Mypassword123"
        }
        ```
    - Response:
        - Succsee: { "success": True }, 200
        - Username format incorrect: {
                "success": "False"
                "reason": "Username format is incorrect."
            }, 400
        - Password format incorrect: {
                "success": "False"
                "reason": "Password format is incorrect."
            }, 400
        - Username exists: {
                "success": "False"
                "reason": "Username already exists."
            }, 400
        - Payload format error: {
                "success": "False"
                "reason": "Incorrect input format"
            }, 400
- Verify account
    - URL: http://localhost:8000/account/verify
    - Method Type: GET
    - Payload:
        ```
        {
            "username": "myusername",
            "password": "Mypassword123"
        }
        ```
    - Response:
        - Succsee: { "success": True }, 200
        - Username or password is incorrect.: {
                "success": "False"
                "reason": "Username format is incorrect."
            }, 400
        - Faied 5 times: {
                "success": "False"
                "reason": "You have tried 5 times, and try again a minute later."
            }, 400
        - Failed to update data: {
                "success": "False"
                "reason": "Update fail."
            }, 400
        - Payload format error: {
                "success": "False"
                "reason": "Incorrect input format"
            }, 400