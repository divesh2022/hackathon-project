CREATE PROCEDURE ValidateLogin
    @role_name VARCHAR(50),
    @user_id INT,
    @phone_number VARCHAR(15)
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1 FROM UserLogin
        WHERE role_name = @role_name AND user_id = @user_id AND phone_number = @phone_number AND is_active = 1
    )
    BEGIN
        PRINT 'Login successful';
    END
    ELSE
    BEGIN
        RAISERROR('Invalid credentials or inactive user.', 16, 1);
    END
END;
