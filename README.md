# Django Interview

Welcome to the live‑coding stage of our hiring process.
You will work on a compact yet production‑style Django REST project. Issues reported by product, marketing, and finance have been turned into auto-tests.

**Your goal is to address those issues and keep all tests green.**

### What's included

- A ready‑to‑run Django application.
- Pre‑configured infrastructure (PostgreSQL, Redis, Docker, devcontainer).
- A comprehensive test suite. All tests should stay green.

## Business stories to address

[See the task list](docs/tasks.md)

## Requirements
- All tests must be successfully passed. For `tests/interview/`, the removal of the decorator `@pytest.mark.xfail` is mandatory.
- Your solution will be evaluated externally. In addition to test results, the following aspects will be considered:
    - code quality and style
    - architectural and implementation decisions
    - adherence to industry best practices
    - the amount of time invested in completing the task
- Creative solutions are welcome if they meet quality standards.

### ⏱ Time‑box

The task is designed to be solved not more than **1 hour**. Focus on clear, incremental fixes.
One hour after the start, access to the interview will be closed.

### Helpful commands

Use the terminal to run:

- `make interview` to run interview tests to check your solutions.
- `make test` to run common project tests to ensure that common features are still working.
- `make lint` to run linters and formatters.
- see more useful commands in the `Makefile`.

Good luck and enjoy!

## About Project

A backend service for an online artisan marketplace connecting local producers and customers. The platform enables vendors to manage their profiles and product listings, while customers can browse, filter, and purchase unique handmade goods. Carts are managed with Redis for performance, and checkout workflows ensure consistency through transactional stock updates. This service is aimed at supporting real business operations such as multi-vendor order handling, inventory control, and secure customer-vendor communication.

[see more details](docs/)

### Tech Stack

- Python: 3.11
- Django: 4
- API: Django REST Framework
- Database: PostgreSQL 15
- Caching: Redis 7
- Testing: Pytest, Pytest-Django
- Architecture: Service Pattern, Resource-Based API
- Dependency Management: `requirements.txt`


### Project Structure Overview
```bash
> tree -a --gitignore /app 
.
├── .env.example
├── Dockerfile
├── Makefile
├── README.md
├── app
│   ├── api
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── services.py
│   └── tasks.py
├── config
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── docs
│   └── README.md
├── manage.py
├── pyproject.toml
├── requirements.txt
└── tests
    ├── api
    │   ├── test_analytics_api.py
    │   ├── test_auth_api.py
    │   ├── test_cart_checkout_api.py
    │   ├── test_heapth.py
    │   └── test_vendor_product_api.py
    ├── conftest.py
    ├── test_services.py
    └── test_vendor_product_models.py

8 directories, 30 files

```

---
Contact: [info@unicheck.ai](mailto:info@unicheck.ai)