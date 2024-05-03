# CIT Project

## Project Description

The objective of this project is to create a program capable of updating a Google Excel sheet at 5-minute intervals with a list of choosen cryptocurrencies and their respective price in USDT and EUR.

## Prerequisites

*Here will be all the information you have to know before using the project*
One of the future additions to plan for would be adding a domain name and a database to enable accessing the API from outside the machine on which it is running.
## Build

*This step should be done once you have met all the prerequisites.*

To start this project, simply execute the bash script using the following command:

```sudo ./build.sh```

To see all the options allowed with this script, use:

```sudo ./build.sh --help```

## CIT API

### Overview

The CIT API enables real-time retrieval of data for a variety of cryptocurrencies (Symbol, price in USDT, and price in EUR). The API also supports applying a filtering system to focus only on the cryptocurrencies of interest.

### Authentication

Since this API is currently running locally on the machine, no authentication is required by the API.

### URI and Versioning

I hope to improve the API over time. Actually the API don't use versioning maybe it will soon. This first iteration will have URIs prefixed with ```http://localhost:8000/api/``` and is structured as described below. There is currently no rate limit.

One of the future additions to plan for would be adding a domain name and a database to enable accessing the API from outside the machine on which it is running.

### Swagger

To access the Swagger and test the API yourself, go to: ```http://localhost:8000/docs```

### Items

All items have the following properties:

Field | Description
------|------------
symbol | The cryptocurrency symbol (Example: Bitcoin -> BTCUSDT).
value_usd | The cryptocurrency price in $ (USDT).
value_eur | The cryptocurrency price in € (EUR).

#### \[GET\]

List all the items of the API.

- **Request**: ```http://localhost:8000/api/items```
- **Response**:
    - status-code: <200>
    - response content: API items list
```javascript
{
    "0": {
        "symbol" : "ETHBTC",
        "value_eur" : "0.008562",
        "value_usd" : "0.007895"
    },
    "1": {
        "symbol" : "BTCUSDT",
        "value_eur" : "55008.44",
        "value_usd" : "54444.44"
    }
    ...
}
```

### Filter

The filtered items have the same properties as the items.

#### \[GET\]

List all the filtered items of the API.

- **Request**: ```http://localhost:8000/api/filter```
- **Response**:
    - status-code: <200>
    - response content: API filtered items list

*With elements in the filtered item list:*
```javascript
{
    "0": {
        "symbol" : "ETHBTC",
        "value_eur" : "0.008562",
        "value_usd" : "0.007895"
    },
    ...
}
```
*Without:*
```javascript
{}
```

#### \[POST\]

Add element to the filtered items list of the API.

- **Request**: ```http://localhost:8000/api/filter/{symbol}```
- **Response**:
    - status-code: <200>
    - response content: API filtered items list with new item

*Before request:*
```javascript
{}
```
*After request with /filter/ETHBTC:*
```javascript
{
    "0": {
        "symbol" : "ETHBTC",
        "value_eur" : "0.008562",
        "value_usd" : "0.007895"
    },
}
```

#### \[DELETE\]

Remove element from the filtered items list of the API.

- **Request**: ```http://localhost:8000/api/filter/{symbol}```
- **Response**:
    - status-code: <200>
    - response content:  API filtered items list without the item

*Before request:*
```javascript
{
    "0": {
        "symbol" : "ETHBTC",
        "value_eur" : "0.008562",
        "value_usd" : "0.007895"
    },
}
```
*After request with /filter/ETHBTC:*
```javascript
{}
```