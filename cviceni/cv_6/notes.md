# Notes

Trivrstva architektura: prezentacni vrstva, business logic, datova vrstva

Mame databazi, tak je obalena business logikou(mame tady logiku (treba pulka), monitoring, logy) a potom ta business je obalena prezentanci. (REST API, gRPC, GraphQL)

## Projekt (cviceni)

GET review (seznam)
POST review (vytvoreni)

Review:
    - id
    - text
    - coffee_shop_id
    - date
    - rating (number of stars)
    - user_id

V databazi by to vypadalo tak:
tabulka kavaren (pro zacatek id kavarny), tabulka review (review_id, created_at, rating), tabulka uzivatelu (pro zacatek staci id) 

Budeme mit mikroservisy. Plus kod rozdelujeme na moduly

## VSCode Extensions

- Python
- REST Client (je dobre pro vyvoj a testovani)
- Even Better TOML

## FastAPI

Musime nadefinovat schema, ktere nam popise nase REST API a aby se to zobrazilo v Swagger docs.

## Postgres

Spustime v Dockeru. Pouzijeme docker-compose, nebot ten nam spusti vice image.
`docker-compose up` - spusti docker, vytvori image a spusti kontejnery. DB je dobre verzovat!

Budeme mit databazovy server a na nem budeme vice databazi (pro kazdy mikroservis).
**Nevytvarej** pomoci Create database v postgres adminer! Ale skrz SQL Command. (ten skript mas v postgres/)

Init script (.sql, .sh) - vykona se pri prvnim spusteni, pouzijeme pro zalozeni dalsi db.

Muzes vytvaret i migracni skripty.