# ecommerce-microservices

Petit projet e-commerce en microservices.

Dedans t'as :

- une gateway Nginx
- un service users
- un service products
- un service orders
- une base Postgres pour chaque service

## Ce qu'il faut

- Docker
- Docker Compose

## Comment lancer le projet

Tu te mets a la racine du repo et tu lances :

```bash
docker compose up -d --build
```

Apres ca, tu peux ouvrir :

```text
http://localhost
```

Le front HTML est servi par la gateway.

## Si tu veux tout couper

```bash
docker compose down
```

Si tu veux aussi supprimer les donnees des bases :

```bash
docker compose down -v
```

## Si t'as modifie un service

Relancer juste la gateway :

```bash
docker compose restart gateway
```

Rebuild un service :

```bash
docker compose up -d --build users-service
```

Tu peux remplacer `users-service` par `products-service`, `orders-service` ou `gateway`.

## Les urls utiles

- Front : `http://localhost`
- Users : `http://localhost/api/users`
- Products : `http://localhost/api/products`
- Orders : `http://localhost/api/orders`

## Exemples rapides

Voir les produits :

```bash
curl http://localhost/api/products
```

Creer un produit :

```bash
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Laptop\",\"price\":1200,\"stock\":5}"
```

Creer un utilisateur :

```bash
curl -X POST http://localhost/api/users \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Alice\",\"email\":\"alice@example.com\",\"password\":\"secret\"}"
```

## En gros

Le point d'entree c'est la gateway.

Donc :

- le front est sur `http://localhost`
- les appels API passent par `http://localhost/api/...`
- les bases sont internes a Docker
