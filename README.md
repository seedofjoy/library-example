library-example
===============


### manage.py commands:


``` drop_all ``` - Drops all tables.

``` load_fixtures ``` - Installs test data fixtures into the database

```shell``` - Runs a Python shell inside Flask application context.

```create_db``` - Creates database tables

``` runserver ``` -  Runs the local server

### First run:

1. Initialize database:
  ```sh
$ manage.py create_db
  ```

2. Insert test data into the database:
  ```sh 
$ manage.py load_fixtures 
   ```

3. Run server:
  ```sh 
$ manage.py runserver 
  ```

### Test account:
Email: **test@test.com**
Password: **123**
