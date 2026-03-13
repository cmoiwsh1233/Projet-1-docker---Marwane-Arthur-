# ecommerce-microservices

Architecture microservices simple avec :

- une gateway Nginx
- trois APIs Flask : `users-service`, `products-service`, `orders-service`
- trois bases PostgreSQL dédiées

## Prerequis

- Docker
- Docker Compose

## Lancer le projet

Depuis la racine du repo :

```bash
docker compose up -d --build
```

La gateway sera disponible sur :

```text
http://localhost
```

## Arreter le projet

```bash
docker compose down
```

Pour arreter et supprimer aussi les volumes PostgreSQL :

```bash
docker compose down -v
```

## Redemarrer un service

Exemple pour la gateway :

```bash
docker compose restart gateway
```

Exemple pour rebuild un service :

```bash
docker compose up -d --build products-service
```

## Architecture

Services exposes via la gateway :

- `/api/users`
- `/api/products`
- `/api/orders`

Bases de donnees internes :

- `postgres-users`
- `postgres-products`
- `postgres-orders`

Les bases PostgreSQL ne sont pas exposees a l'exterieur. Elles communiquent uniquement sur le reseau Docker `ecommerce-network`.

## Exemples de requetes

### Healthcheck

```bash
curl http://localhost/api/users/health
curl http://localhost/api/products/health
curl http://localhost/api/orders/health
```

### Creer un produit

```bash
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Laptop\",\"price\":1200,\"stock\":5}"
```

### Lister les produits

```bash
curl http://localhost/api/products
```

### Creer un utilisateur

```bash
curl -X POST http://localhost/api/users \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Alice\",\"email\":\"alice@example.com\",\"password\":\"secret\"}"
```

## Fichiers principaux

- `compose.yaml` : orchestration Docker Compose
- `gateway/nginx.conf` : configuration de la gateway Nginx
- `users-service/app.py` : API Users
- `products-service/app.py` : API Products
- `orders-service/app.py` : API Orders
