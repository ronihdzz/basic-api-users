# Basic API Users

| CI Status | Coverage |
|-----------|----------|
| ![CI](https://github.com/ronihdzz/basic-api-feelings/actions/workflows/ci.yml/badge.svg) | ![Coverage Badge](https://github.com/ronihdzz/basic-api-feelings/raw/artifacts/main/latest/coverage.svg) |

## Overview

This API provides functionality to manage users, including creating accounts, authentication, retrieving user information, and deleting accounts. It uses JWT for secure authentication.


### Endpoints


#### 1. Create User

* Method: `POST`
* Path: `/v1/users/`
* Description: Registers a new user.
* Request Body
    ```
    {
    "username": "string",
    "email": "string",
    "password": "string"
    }
    ```
* Response 
    ```
    {
    "id": "integer",
    "username": "string",
    "email": "string"
    }
    ```
* Erros:
    * `400 Bad Request`: Username or email already registered.


#### 2. Obtain Token

* Method: `POST`
* Path: `/v1/token/`
* Description: Authenticates a user and returns a JWT token.
* Request Body
    ```
    {
    "username": "string",
    "password": "string"
    }
    ```
* Response 
    ```
    {
    "access_token": "string",
    "token_type": "bearer"
    }
    ```
* Erros:
    * `401 Unauthorized`: Incorrect username or password.


#### 3. Get Current User

* Method: `GET`
* Path: `/v1/users/me/`
* Description: Retrieves information of the authenticated user.
* Headers:
    ```
    Authorization: Bearer <access_token>
    ```
* Response 
    ```
    {
    "id": "integer",
    "username": "string",
    "email": "string"
    }
    ```
* Erros:
    * `401 Unauthorized`: Invalid or expired token.
    * `401 Unauthorized`: User not found or deleted.


#### 4. Create User


* Method: `DELETE`
* Path: `/v1/users/me/`
* Description: Deletes the account of the authenticated user.
* Headers:
    ```
    Authorization: Bearer <access_token>
    ```
* Response 
    ```
    {
    "detail": "User deleted"
    }
    ```
* Erros:
    * `401 Unauthorized`: Invalid or expired token.
    * `401 Unauthorized`: User not found or deleted.

## Configuration and Execution

### Local Environment

#### 1) Run the Project

Navigate to the `src` folder and execute the following command:

```
uvicorn main:app --reload
```

#### 2) Run Project Tests


Navigate to the `src` folder and execute the following command:

```
pytest tests
```

#### 3) Run Test Coverage

Navigate to the src folder and execute the following command:

```
coverage run -m pytest tests -s -v --lf && coverage report
```

### Using Docker Compose

#### 1) Run the Project

```
docker-compose up app
```

#### 2) Run the Tests

```
docker-compose run test
```

## Environment Variables Required

* `ENVIRONMENT`: Indicates the environment in which the application is running (e.g., development, production, test).
* `DATABASE_NAME`: Name of the SQLite database (e.g., prod.db, test.db).
* `PRIVATE_KEY`: RSA private key for signing JWT tokens.
* `PUBLIC_KEY`: RSA public key for verifying JWT tokens.
* `JWT_ALGORITHM`: Algorithm used for signing JWT tokens (e.g., RS256).
* `JWT_EXPIRATION_MINUTES`: Token expiration time in minutes.

## Generate keys public and private:

```
openssl genpkey -algorithm RSA -out private_key.pem && openssl rsa -pubout -in private_key.pem -out public_key.pem
```




## GitHub Workflow

### GitHub Workflow Explanation

This GitHub Actions workflow automates the process of testing, building, and deploying Docker images for the Basic API Feelings project. Below is a step-by-step explanation of what the workflow does:

### Workflow Steps

1. **Triggering Events**
   - The workflow is triggered on `push` and `pull_request` events to the `main`, `development`, and `staging` branches.

2. **Test Job**
   - **Checkout code**: The code is checked out from the repository.
   - **Set up Docker Buildx**: Docker Buildx is configured for building images.
   - **Cache Docker layers**: Docker layers are cached to speed up subsequent builds.
   - **Build and run tests**: Docker image is built using the test Dockerfile, and tests are executed inside the container.
   - **Save artifacts**: Test reports are saved to an `artifacts` branch for further analysis.

3. **Push Docker Hub Job**
   - **Checkout code**: The code is checked out from the repository.
   - **Set environment variables**: The environment (production, development, staging) is set based on the branch.
   - **Login to Docker Hub**: Authentication to Docker Hub using the provided secrets.
   - **Set Docker image version**: A unique version tag is generated using the current UTC date and time.
   - **Pull existing images**: The latest Docker image is pulled, and a rollback tag is created if the image exists.
   - **Build Docker image**: The Docker image is built and tagged with the version and latest tags.
   - **Run Docker container to test**: The Docker image is tested by running it in a container.
   - **Push Docker image**: The Docker image is pushed to Docker Hub.

4. **Push DigitalOcean Job**
   - **Checkout code**: The code is checked out from the repository.
   - **Set environment variables**: The environment (production, development, staging) is set based on the branch.
   - **Login to DigitalOcean Container Registry**: Authentication to DigitalOcean using the provided token.
   - **Set Docker image version**: A unique version tag is generated using the current UTC date and time.
   - **Pull existing images**: The latest container image is pulled, and a rollback tag is created if the image exists.
   - **Build Docker image**: The Docker image is built and tagged with the version and latest tags.
   - **Run Docker container to test**: The Docker image is tested by running it in a container.
   - **Push Docker image**: The Docker image is pushed to DigitalOcean Container Registry.



### GitHub Workflow Environment Variables and Secrets

This project uses several environment variables and secrets for continuous integration (CI) and deployment within the GitHub workflow. Below is a list of these variables and secrets, along with their descriptions:

#### Secrets

1. **GH_TOKEN**
   - **Description**: A personal access token for GitHub. It is used to authenticate with the GitHub API to perform various actions such as cloning repositories, pushing changes, and managing artifacts.
   - **Importance**: Essential for CI workflows to interact securely with GitHub repositories.

2. **DOCKERHUB_USERNAME**
   - **Description**: The username for Docker Hub. It is used to log in to Docker Hub to push and pull Docker images.
   - **Importance**: Necessary for authenticating with Docker Hub to manage Docker images.

3. **DOCKERHUB_PASSWORD**
   - **Description**: The password for Docker Hub. It is used in conjunction with `DOCKERHUB_USERNAME` to log in to Docker Hub.
   - **Importance**: Required for secure access to Docker Hub to push and pull Docker images.

4. **DIGITALOCEAN_TOKEN**
   - **Description**: A token for accessing the DigitalOcean Container Registry. It is used to authenticate with DigitalOcean to push and pull container images.
   - **Importance**: Needed for secure operations with the DigitalOcean Container Registry.

#### Environment Variables

1. **DOCKERHUB_REPOSITORY**
   - **Description**: The name of the Docker Hub repository where the Docker images are stored.
   - **Importance**: Specifies the target repository for Docker images, ensuring they are pushed to the correct location.

2. **DIGITALOCEAN_REPOSITORY**
   - **Description**: The name of the DigitalOcean Container Registry repository where the container images are stored.
   - **Importance**: Identifies the correct repository in DigitalOcean for storing and retrieving container images.

