# Doc to PDF Project

This project provides a web application that converts `.docx` files to `.pdf` files. The backend is built using FastAPI, and the frontend is a React-based application. Docker is used for easy deployment.

## Table of Contents
- [Installation](#installation)
  - [Frontend Installation](#frontend-installation)
  - [Backend Installation](#backend-installation)
  - [Using Docker](#using-docker)
- [Usage](#usage)
- [License](#license)

## Installation


## Using Docker

You can also use Docker to run both the frontend and backend in containers using Docker Compose.

### Run with Docker Compose

1. **For the first time**, to build the images and start the services:

    ```bash
    docker-compose up --build
    ```

2. **For subsequent runs**, to start the services without rebuilding:

    ```bash
    docker-compose up
    ```

This will spin up both the frontend and backend services, and they will be accessible at:
Frontend on port 3000 
Backend on port 8000

---
### Frontend Installation(without docker)

To set up the frontend locally:

1. Navigate to the frontend directory:

    ```bash
    cd doc_to_pdf
    ```

2. Install the required npm packages:

    ```bash
    npm install
    ```

3. Start the frontend server:

    ```bash
    npm run start
    ```

The frontend will now be available at port [3000](http://localhost:3000).

---

### Backend Installation(without docker)

To set up the backend locally:

1. Navigate to the backend directory:

    ```bash
    cd backend
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the FastAPI backend server:

    ```bash
    uvicorn main:app --reload
    ```

The backend will be available at port [8000](http://localhost:8000).

---

## Usage

Once the application is running, you can upload a `.docx` file through the frontend, and it will be converted to a `.pdf` file by the backend. The converted `.pdf` can then be downloaded.

