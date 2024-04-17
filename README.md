# AtomFit

## Description
AtomFit is a fitness app designed for aiding you in your workouts. Made with Poetry and FastAPI the app is the perfect companion for any exercise or workout, having multiple features for varying your exercises, tracking calories and workouts


## Installation
1. Clone the repository:
```
git clone https://github.com/AtomFit/AtomFit-Backend
```
2. Navigate to the project directory:
```
cd src
```
3. Install poetry:
```
pip install poetry
```
4. Run poetry config:
```
poetry install 
```

## Configuration
1. Create a new database in PostgreSQL:
```
CREATE DATABASE AtomFit;
```
2. Write .env file with the following content:
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/atomfit
STAGE=dev
```
3. Run the database migrations:
```
alembic upgrade head
```
## Usage
1. Start the FastAPI server:
```
uvicorn main:app --reload
```
2. Access the API documentation at `http://localhost:8000/docs` to explore available endpoints and interact with the application.

3. Access admin panel at `http://localhost:8000/admin/login` to manage products and categories.

## API Endpoints
You can see the API documentation at `http://localhost:8000/docs` to explore available endpoints and interact with the application.

## Contributing
Contributions are welcome for personal use, but due to it being a project destined for a school program we don't encourage them. If you'd like to contribute to AtomFit, please fork the repository and submit a pull request with your changes.


## Credits
AtomFit was created by Casciuc Stanislav, Robu Gabriel, Crintea Sebastian and Rusu Sebastian. Special thanks to the FastAPI team for providing an excellent framework for building APIs, and for the Poetry team.

