# Defect Reports

These defects are built into the demo app and are active when it is started with `SEEDED_BUGS=true`.
With the bugs on, 8 of the 38 tests fail (5 API, 3 UI); with the clean build all 38 pass.

---

## BUG-001: Product search is case-sensitive
- **Severity:** Medium | **Priority:** Medium
- **Environment:** Demo shop, `SEEDED_BUGS=true`
- **Steps to reproduce**
  1. Open `/products` after logging in (or call `GET /api/products?q=backpack`).
  2. Search for `backpack` (lowercase).
- **Expected:** "Backpack" is returned (search ignores case).
- **Actual:** No products found; only the exact spelling `Backpack` matches.
- **Impact:** Customers who type in lowercase get an empty result and may leave.
- **Detected by:** `test_search_is_case_insensitive` (API, 3 variants) and the UI test of the same name.

## BUG-002: Cart total ignores item quantity
- **Severity:** High | **Priority:** High
- **Steps to reproduce**
  1. Log in and add 3 x "Bike Light" (9.99 EUR each) to the cart.
  2. Open the cart (or call `GET /api/cart`).
- **Expected:** Total = 29.97 EUR.
- **Actual:** Total = 9.99 EUR (quantity is not multiplied).
- **Impact:** Customers are under-charged; direct revenue loss.
- **Detected by:** `test_cart_total_takes_quantity_into_account` (API) and `test_cart_total_reflects_quantity` (UI).

## BUG-003: Checkout accepts an empty address
- **Severity:** High | **Priority:** Medium
- **Steps to reproduce**
  1. Add any product to the cart and open checkout.
  2. Enter a name, leave the address empty, and place the order.
- **Expected:** Error "Name and address are required"; no order is created.
- **Actual:** The order is created without a delivery address.
- **Impact:** Orders cannot be delivered; manual follow-up needed.
- **Detected by:** `test_checkout_requires_address` (API) and the UI test of the same name.
