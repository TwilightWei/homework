# Requirements
- Docker

# Deployment Process
1. cd to project root directory.
2. Build images "docker-compose -f docker-compose.yml up -d --build"
3. Connect to mysql db with the following credential.
    - Host: localhost
    - Username: root
    - Password: root
    - Port: 8080
4. Initialize the database with the following scripts.
    ```
    CREATE DATABASE homework;
    USE homework;

    CREATE TABLE `customer`(
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `phone` VARCHAR(20) UNIQUE,
        `email` VARCHAR(50) UNIQUE,
        `password` VARCHAR(100),
        `updated_at` DATETIME NOT NULL,
        `created_at` DATETIME NOT NULL
    );

    CREATE TABLE `commodity`(
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(50) NOT NULL,
        `cost` INT UNSIGNED NOT NULL,
        `updated_at` DATETIME NOT NULL,
        `created_at` DATETIME NOT NULL
    );

    CREATE TABLE `point`(
        `customer_id` INT UNSIGNED NOT NULL,
        `amount` INT NOT NULL,
        `updated_at` DATETIME NOT NULL,
        `created_at` DATETIME NOT NULL,
        PRIMARY KEY (customer_id),
        FOREIGN KEY (customer_id) REFERENCES customer(id)
    );

    CREATE TABLE `point_change_history`(
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `customer_id` INT UNSIGNED NOT NULL,
        `amount` INT NOT NULL,
        `action` VARCHAR(20) NOT NULL,
        `created_at` DATETIME NOT NULL
    );

    INSERT INTO `customer`
    (`id`, `phone`, `email`, `password`, `updated_at`, `created_at`)
    VALUES
    (1, '0922123456', 'test@gmail.com', 'encryptedpassword', '2023-01-01 00:00:00', '2023-01-01 00:00:00');

    INSERT INTO `point`
    (`customer_id`, `amount`, `updated_at`, `created_at`)
    VALUES
    (1, 0, '2023-01-01 00:00:00', '2023-01-01 00:00:00');

    INSERT INTO `commodity`
    (`name`, `cost`, `updated_at`, `created_at`)
    VALUES
    ('Pen', 100, '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
    ('Cup', 200, '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
    ('Backpack', 500, '2023-01-01 00:00:00', '2023-01-01 00:00:00');
    ```
5. Restart flask container "docker-compose -f docker-compose.yml up -d flask"

# APIs
- Add point
    - URL: http://localhost:8000/point/1/add
    - Method Type: PUT
    - Payload:
        ```
        {
            "amount": 1000
        }
        ```
    - Response:
        - Succsee: { "message": "success" } 200
        - Failed: { "message": "Failed" } 400
- Redeem point
    - URL: http://localhost:8000/point/1/redeem
    - Method Type: PUT
    - Payload:
        ```
        {
            "commodities": [
                {
                    "commodity_id": 1,
                    "amount": 3
                },
                {
                    "commodity_id": 3,
                    "amount": 1
                }
            ]
        }
        ```
    - Response:
        - Succsee: { "message": "success" } 200
        - Failed: { "message": "Failed" } 400