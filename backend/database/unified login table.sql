CREATE TABLE UserLogin (
    login_id INT IDENTITY PRIMARY KEY,
    role_name VARCHAR(50),         -- e.g., 'Doctor', 'ASHAWorker', etc.
    user_id INT,                   -- Matches the primary key in the role-specific table
    phone_number VARCHAR(15),      -- Used for login
    email VARCHAR(100),            -- Optional for future use
    password_hash VARCHAR(255),    -- Placeholder for future password-based login
    is_active BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE()
);
