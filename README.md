# Ecommerce Microservices

This project is an e-commerce platform built with Django, using a microservices architecture. It contains separate services for **User Management** and **Product Management**, with PostgreSQL databases for each. These services communicate with each other and run in isolated containers using Docker.

## Project Structure

The project is organized into two services:

1. **User Service**: Handles user authentication, registration, and profile management.
2. **Product Service**: Manages products, categories, and product reviews.

### Project Directory Structure

```plaintext
ecommerce_microservices/
├── user_service/
│   ├── Dockerfile
│   ├── manage.py
│   ├── user_service/
│   │   ├── settings.py
│   │   ├── ...
│   ├── users/
│   ├── requirements.txt
│   ├── .env
├── product_service/
│   ├── Dockerfile
│   ├── manage.py
│   ├── product_service/
│   │   ├── settings.py
│   │   ├── ...
│   ├── products/
│   ├── requirements.txt
│   ├── .env
├── docker-compose.yml



Requirements
Docker: For containerizing the services and databases.
Docker Compose: For managing multi-container Docker applications.
