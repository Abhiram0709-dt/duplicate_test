# ShopCore

ShopCore is a small backend-style Python project that simulates checkout, pricing, inventory, payment, shipping, and notifications.

It is intentionally simple to run and intentionally rich in history so it can be used for commit-classification experiments.

The checkout preview path includes an in-memory cache keyed by cart contents, shipping country, and promotion code.

Batch checkout previews are also available for back-office review flows that need to inspect several carts at once.
