# Ikusi backend transactions

Microservicio encargado de la administración de trasacciones asociadas a un usuarios de la aplicacion Ikusi.

## Endpoints

| Endpoint  | Headers  |  Body keys | HTTP method |
|:---:|:---:|:---:|:---:|
| `/transactions`  | `Authorization` Bearer  |  `amount`, `concept` |  POST |
| `/transactions/me`  |   | `username`, `password`  |  POST |
| `/validate-token`  | `token`  |   |  GET |