# Documenting the FastAPI CSV Uploader App: A Guide to Building and Deploying a Web Application for Uploading and Viewing CSV Files

## Introduction
This documentation outlines the features, functionalities, and usage of a web application built with Python, FastAPI, and SQLite. The web application is a CSV file management system that allows users to upload, view, modify, and delete CSV files. It also has an authentication and authorization system that ensures the security and privacy of the files.

The application has been designed and developed to be user-friendly, efficient, and scalable. It provides an intuitive user interface that makes it easy for users to navigate and perform tasks. The application also uses best practices and standards for web development to ensure compatibility, reliability, and maintainability.

This documentation is intended for users, developers, and administrators who want to understand the features and usage of the application. It provides a detailed overview of the application's architecture, components, and functionalities. It also includes instructions on how to install, configure, and use the application.

## Technologies Used
The following technologies were used in the development of this app:

> Python
> FastAPI
> SQLAlchemy
> Jinja2
> HTML
> CSS
> JavaScript

## Installation
1. Clone the repository:
`git clone https://github.com/yourusername/your-repo-name.git`
2. Change directory to the project folder:
`cd your-repo-name`
3. Install the required dependencies:
`pip install -r requirements.txt`
4. Create a .env file in the root directory and add the following environment variables:
`
DATABASE_URL="postgresql://db_user:db_password@localhost/db_name"
JWT_SECRET_KEY="your_secret_key"
`
5. Run the database migrations:
`python database.py`
6. Start the server:
`python main.py`
7. Open the application in your browser at http://localhost:8000.

## Authentication and Authorization
This application has a user authentication and authorization system implemented using JSON Web Tokens (JWTs). Users can create an account by providing their email and a password. The password is hashed using the bcrypt library and stored in the database. When a user logs in, their credentials are verified and a JWT is generated and returned to the client.

The JWT is then included in subsequent requests to protected endpoints in the application. The server verifies the JWT before allowing access to the protected endpoint. This ensures that only authorized users can access protected resources.

The JWT has an expiration time of 30 minutes. After 30 minutes, the user must log in again to generate a new JWT. The expiration time can be configured in the config.py file.

To ensure that a user can only access their own uploaded files, the user's ID is included in the CSV file model. When a user uploads a file, their ID is associated with the file in the database. When listing or deleting files, the server checks that the user making the request is the same user who uploaded the file.

## Endpoints
The following endpoints are available in the application:

/signup - This endpoint is used to create a new user. The user must provide a valid email address and a password. If the email address is already registered, the endpoint will return an error message.

/login - This endpoint is used to log in an existing user. The user must provide a valid email address and password. If the email address or password is incorrect, the endpoint will return an error message.

/csv - This endpoint is used to upload a CSV file. The file must be in CSV format and must be less than 250MB in size. The endpoint requires the user to be authenticated.

/csv/{csv_file_id}/view - This endpoint is used to view a CSV file. The endpoint requires the user to be authenticated and authorized to view the file.

/csv/{csv_file_id}/column/{column_id} - This endpoint is used to modify the name of a column in a CSV file. The endpoint requires the user to be authenticated and authorized to modify the file.

/csv/{csv_file_id}/delete - This endpoint is used to delete a CSV file. The endpoint requires the user to be authenticated and authorized to delete the file.

/csv/list - This endpoint is used to list all the CSV files uploaded by the user. The endpoint requires the user to be authenticated.

## Error Handling
* 400 Bad Request  
This error occurs when the server cannot understand the request due to invalid syntax. It can be caused by malformed requests or invalid parameters.
In this case, the server will respond with a JSON object containing an error message to inform the user of the issue.


* 401 Unauthorized  
This error occurs when the user tries to access a resource without providing valid authentication credentials.
In this case, the server will respond with a JSON object containing an error message asking the user to authenticate themselves.


* 403 Forbidden  
This error occurs when the user is authenticated, but they do not have sufficient permissions to access the requested resource.
In this case, the server will respond with a JSON object containing an error message informing the user that they do not have the required permissions.


* 404 Not Found  
This error occurs when the server cannot find the requested resource.
In this case, the server will respond with a JSON object containing an error message informing the user that the requested resource does not exist.


* 405 Method Not Allowed  
This error occurs when the user tries to use an HTTP method that is not supported by the server.
In this case, the server will respond with a JSON object containing an error message informing the user that the requested method is not allowed.


* 500 Internal Server Error  
This error occurs when the server encounters an unexpected condition that prevents it from fulfilling the request.
In this case, the server will respond with a JSON object containing an error message informing the user that an internal server error has occurred.

## Future Improvements
1. User roles and permissions:  
Currently, the app only has two user roles - admin and regular user. Adding more granular user roles and permissions, such as read-only access, would improve the security and usability of the app.

2. File validation:  
The app currently allows users to upload any file type, which could potentially pose a security risk. Adding file validation to only allow CSV files would be a good improvement.

3. Search functionality:  
Adding search functionality to allow users to search for specific files by name, size, or upload date would improve the usability of the app.

4. Improved UI:  
The current UI is basic and could be improved to provide a better user experience. Adding more interactive features and a better design would make the app more user-friendly.

5. Pagination:  
Currently, all uploaded files are displayed on one page, which can become unwieldy with a large number of files. Implementing pagination would help to improve the app's performance and usability.

6. File Editing:  
Implementing the ability for users to edit CSV files within the app, rather than just viewing them, would make the app more useful.

7. API integration:  
Adding API integration would allow users to retrieve and upload CSV files from external sources, providing a more flexible and robust solution.

## Conclusion
In conclusion, this app provides a simple and easy-to-use interface for uploading, viewing, and modifying CSV files. The use of Python FastAPI framework and technologies such as HTML, CSS, and JavaScript make the app versatile and easily customizable. The app's modular architecture allows for easy addition of features, making it a suitable starting point for building more complex data management systems. The app also provides a good example of how to implement authentication and authorization in a FastAPI application. Future improvements could include features such as data visualization, export to different file formats, and more robust error handling. Overall, this app serves as a good foundation for building data-driven web applications.

