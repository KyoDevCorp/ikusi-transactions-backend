# Ikusi backend transactions

Microservicio encargado de la administración de trasacciones asociadas a un usuarios de la aplicacion Ikusi.

## Endpoints

### Descripción de los endpoints

- `/transactions`: Permite crear una transacción asociandola a un usuario previamente creado por medio del JWT de registro o inicio de sesión.

- `/transactions/me`: Obtiene un array con todas las transacciones asociadas a un usuario.

- `/validate-token`: Genera un resumen y analisis de las transacciones de un cliente, entregando clasificación por concepto, totales por concepto y totales globales.

### Configuración y uso de enpoints

| Endpoint  | Headers  |  Body keys | HTTP method |
|:---:|:---:|:---:|:---:|
| `/transactions`  | `Authorization` Bearer  |  `amount`, `concept` |  POST |
| `/transactions/me`  |  `Authorization` Bearer |   |  GET |
| `/transactions/me/analytics`  | `Authorization` Bearer  |   |  GET |