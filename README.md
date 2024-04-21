# Authentication and Profile Service Documentation

## Overview
This documentation outlines the components, Docker configurations, and FastAPI endpoints implemented in the `auth_profile_service` for the BQP Assignment platform. The service is designed to manage authentication and user profile operations, enabling users to login, manage profiles, and handle follower relationships in a secure and scalable manner.

## Directory Structure

    /auth_profile_service
    ├── /compose
    │   └── /local
    │       ├── Dockerfile             # Dockerfile to build the Docker image
    │       └── start                  # Startup script to launch the FastAPI server
    ├── /src
    │   ├── database.py                # Defines database models and ORM configurations
    │   ├── main.py                    # FastAPI application entry point
    │   ├── requirements.txt           # Lists Python dependencies
    │   ├── entities.py                # Pydantic models for user data validation
    │   └── /config
    │       ├── .env                   # Stores environment variables
    │       └── constants.py           # (Optional) Stores constants used across the application
    └── local.yml                      # Docker Compose configuration for local development

## Components

### Docker Configuration
- **File**: `local.yml`
- **Description**: Configures the Docker environment for the authentication and profile service, setting up the necessary service parameters, exposed ports, and volume mappings for development.

### Dockerfile
- **Location**: `compose/local/Dockerfile`
- **Purpose**: Builds the Docker image for the service, installing required Python packages and setting up the environment.

### Startup Script
- **File**: `compose/local/start`
- **Purpose**: Executes the FastAPI application using Uvicorn with specified host and port configurations. It ensures that the service reloads automatically during development when changes are detected.

## Source Code Files

### Main Application (FastAPI)
- **File**: `src/main.py`
- **Functionality**:
  - Entry point for the FastAPI application.
  - Defines routes for user authentication, profile management, and follower operations.

### Database Configuration
- **File**: `src/database.py`
- **Functionality**:
  - Establishes database connections using SQLAlchemy.
  - Defines ORM models for users and manages database sessions.

### Entities
- **File**: `src/entities.py`
- **Functionality**:
  - Defines Pydantic models for user creation, update, and follower operations, ensuring data validation.

### Python Requirements
- **File**: `src/requirements.txt`
- **Details**: Includes all necessary Python libraries such as FastAPI, Uvicorn, PyJWT, and others required to run the authentication and profile service.

## Configuration Files

### Environment Variables
- **File**: `src/config/.env`
- **Contains**:
  - Google client credentials and JWT secret key for integration with Google OAuth2 and securing JWT tokens.

### Constants
- **File**: `src/config/constants.py`
- **Description**: This file can store constant values used throughout the application, although it is optional and currently empty.

## Setup and Deployment
To deploy the authentication and profile service locally using Docker:
1. Navigate to the service directory:
    ```bash
    cd /path/to/auth_profile_service
    ```
2. Build and run the Docker container:
    ```bash
    docker-compose -f local.yml up --build
    ```

This setup ensures that the authentication and profile service is properly configured and ready for integration with other services or for standalone functionality as part of the BQP Assignment platform.
