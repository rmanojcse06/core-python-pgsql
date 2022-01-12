**Step(1):** Pull the Docker image <br/>
`docker pull postgres`
<br/>
<br/>
**Step(2):** Check if the image is downloaded<br/>
`docker images`
<br/>
<br/>
**Step(3):** Create a new folder into the current project<br/>
`mkdir -p pgsql_data`
<br/>
<br/>
**Step(4):** Start the postgres image<br/>
`docker run -d -it --name man-flask-dev-pgsql-1 -e POSTGRES_PASSWORD=Pass2022# -v pgsql-data:/var/lib/postgresql/data -p 25432:5432 postgres`
<br/>
<br/>
**Step(5):** Check if the database running in container<br/>
`docker ps --filter "status=running" --filter "name=man-flask-dev-pgsql-1"`
<br/>
`docker ps --filter "status=exited" --filter "name=man-flask-dev-pgsql-1"`
<br/>
<br/>
Check for more filter options at
https://docs.docker.com/engine/reference/commandline/ps/#filtering
<br/>
<br/>
Else try to enter inside the postgres shell.
`docker exec -it man-flask-dev-pgsql-1 bash`
<br/>
<br/>
**Step(6):** Open postgres sql shell command
`psql -h localhost -U postgres`
<br/>
There were some options we can look into using the following link 
- https://www.postgresql.org/docs/13/app-psql.html
- https://docs.sqlalchemy.org/en/14/core/engines.html
<br/>
<br/>

**Step(7):** You can connect pgsql using the following dialect command:
<br/>
`postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]`
<br/>
<br/>



engine = create_engine('postgresql+psycopg2://scenott:tiger@localhost/mydatabase')