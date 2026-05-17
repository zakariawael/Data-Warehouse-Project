CREATE TABLE Dim_Date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week INT,
    day_name VARCHAR(10),
    month INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT
);

CREATE TABLE Dim_Customer (
    customer_key INT PRIMARY KEY,
    customer_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(100),
    email VARCHAR(100),
    active_status VARCHAR(10),
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE Dim_Film (
    film_key INT PRIMARY KEY,
    film_id INT,
    title VARCHAR(255),
    description TEXT,
    release_year INT,
    language VARCHAR(50),
    rental_duration_limit INT,
    rental_rate DECIMAL(5,2),
    length_minutes INT,
    replacement_cost DECIMAL(5,2),
    rating VARCHAR(10),
    category_name VARCHAR(50)
);

CREATE TABLE Dim_Store (
    store_key INT PRIMARY KEY,
    store_id INT,
    store_address VARCHAR(255),
    city VARCHAR(50),
    country VARCHAR(50),
    manager_first_name VARCHAR(50),
    manager_last_name VARCHAR(50)
);

CREATE TABLE Fact_Rental_Payment (
    fact_key INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    film_key INT,
    store_key INT,
    payment_amount DECIMAL(10,2),
    rental_duration_days INT,
    rental_count INT
);