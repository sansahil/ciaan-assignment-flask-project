### How to run this locally

- Run the database container using this command -

```sh
docker run --name postgresql-container -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
```

- Clone the repo to local and run the server

```sh
git clone https://github.com/sansahil/startup-school.git
cd startup-school
python3 app.py runserver
```

- Look for the URL in the browser - `http://127.0.0.1:5000/signup`
- Run the operations in the page, it should work and lead to the dashboard page

### Here is the demo of the progress

[![Watch the video](https://raw.githubusercontent.com/sansahil/ciaan-assignment-flask-project/main/signup_demo.mov)](https://raw.githubusercontent.com/sansahil/ciaan-assignment-flask-project/main/signup_demo.mov)
