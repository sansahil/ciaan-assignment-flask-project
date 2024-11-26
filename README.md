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

![signup_demo-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/86dea753-45a8-4451-b1ca-85ae47ef69ff)

