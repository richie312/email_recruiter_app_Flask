# Application Data Model And Persistence

## Core domain object

`src/objects/Application.py` defines the main `Application` object used by the web app.

It captures:

- `Company`
- `Location`
- `Email Address`
- `Subject`
- `Application_Date`

The class also keeps an in-memory cache through:

- `Application.all_contacts`

This cache supports temporary accumulation of contacts before a later persistence action.

## Persistence behavior

The `Application` object supports:

- `add_details()`: inserts a single application row into MySQL
- `update()`: bulk-persists the in-memory cache using pandas and SQLAlchemy
- `delete()`: deletes rows by company name
- `get_data()`: fetches full application history

There is also a module-level `get_data()` helper that retrieves rows and column metadata from MySQL.

## Database layer

`config/database.py` exposes two access styles:

- direct `mysql.connector` connections for row-based CRUD
- SQLAlchemy engine creation for bulk DataFrame writes

Important database settings are loaded from `.env`:

- `db_host`
- `db_user`
- `db_passwd`
- `dbname`

## User model

User account/profile state is stored via SQLAlchemy in `src/sql/sqlite.py` through the `User` model, which is used in:

- login
- signup
- password reset
- profile rendering
- resume/profile/image upload flows

## Two-path ingestion into MySQL

Based on the current application behavior and your wiki instructions, job data reaches the application database through two main paths:

1. Manual submission through `/addDetails`
2. Automated apply from the job dashboard through `/apply_job`

Both paths eventually create an `Application` object and persist it.
