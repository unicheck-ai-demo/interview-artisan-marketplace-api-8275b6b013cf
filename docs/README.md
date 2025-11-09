# Artisan Marketplace API

A backend service for an online artisan marketplace connecting local producers and customers. Vendors manage profiles and product listings, customers browse/filter/purchase unique goods, and the whole e-commerce cart/checkout pipeline is handled with Redis for performance and transactional DB for consistency.

## Architecture Overview
- **Framework**: Django 4+, Django REST Framework, PostgreSQL + PostGIS, Redis, Celery
- **Layered Design**: Models define DB schema, Services encapsulate business logic, API endpoints (ViewSets, APIViews) handle HTTP routing/data flow.
- **Resource-based API**: Endpoints are organized by domain resources (Vendor, Product, Cart, Order).

## Data Model
- **Vendor**: Linked one-to-one to User. Stores profile, location (PointField for geo queries), contact, and description. Vendors own Products and Orders.
- **Product**: Linked to Vendor. Attributes: name, description, price, quantity, category, image.
- **Order**: Linked to Customer (User) and Vendor. Tracks status, total amount, time stamps, and contains multiple OrderItems for multi-product, multi-vendor purchases.
- **OrderItem**: Linked to Order and Product. Tracks quantity, price, enforces product-stock constraints.
- **Cart**: Not a DB model. All cart data is stored in Redis (per-user key), guaranteeing fast multi-product carts and resilience to server restarts.

## Features
- **Vendor Profile Management**: Register/update vendor with location, contact, description. Search/filter by proximity (using PostGIS queries).
- **Product Catalog CRUD**: Vendors add/edit/remove products. Products filterable by category, price, location.
- **Customer Browsing & Filtering**: Efficient, scalable filtering by category, price range, vendor geo-location via clean service logic and optimized Django ORM.
- **Redis-backed Shopping Cart**: Cart operations use Redis with TTL. Cart is always up-to-date, fast, and robust (products tracked by ID and quantity; full cart returned/read via lightweight API calls).
- **Transactional Checkout**: Upon checkout, row-level locking and transaction atomicity ensure no overselling. Products stock is updated only if quantity is available, order and order items are recorded atomically for all vendors in cart.
- **Order History & Vendor Analytics**: APIs surface vendor sales analytics via aggregate DB queries (including window/aggregate functions for time-scope metrics).

## API Patterns
- **Routers**: `api/vendors/`, `api/products/`, `api/cart/`, `api/checkout/`, `api/vendors/{id}/analytics/`.
- **Serializers**: Used for all data validation, input/output formatting. No business logic in serializers—logic lives in services.
- **Authentication**: All sensitive endpoints secured via DRF TokenAuthentication. Customers/vendors can only access their resources; write ops require valid token.
- **Permissions**: IsAuthenticatedOrReadOnly for CRUD APIs. Write ops for cart/checkout strictly require authentication.

## Key Implementation Notes
- All cart quantities are validated and managed as integers for transactional safety.
- All advanced geo/product filtering leverages select_related/prefetch_related ORM optimizations (no N+1 queries).
- Orders are multi-vendor-capable: Each checkout may produce multiple Order objects, one per vendor.
- Vendor analytics data is aggregated in-database (count, sum).
- Unused files cleaned; code aligns with modern Django/DRF/service best practices.

## Setup/Usage
- Use provided Docker/Codespaces for installation (`make setup`)
- Run tests: `make test`
- Development server: `make run`
- API docs: DRF schema available (DRF Spectacular integration).

## Contact
info@unicheck.ai
