# Itinerary service

## Postgres

```cmd
docker run -d --name postgres-itinerary -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=itinerary_db -p 5432:5432 postgres:latest
```