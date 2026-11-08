# Test Cases (mapped to automated tests)

| ID | Area | Test case | Type | Automated test |
|---|---|---|---|---|
| TC-01 | Auth | Valid login returns a token | API, smoke | `test_login_with_valid_credentials_returns_token` |
| TC-02 | Auth | Wrong password returns 401 | API | `test_login_with_wrong_password_is_rejected` |
| TC-03 | Auth | Locked user returns 423 | API | `test_login_for_locked_user_returns_423` |
| TC-04 | Auth | Missing username/password returns 400 | API | `test_login_with_missing_fields_returns_400` (3 variants) |
| TC-05 | Products | List is not empty and has required fields | API, smoke | `test_product_list_is_not_empty_and_has_required_fields` |
| TC-06 | Products | Get product by id / unknown id returns 404 | API | `test_get_product_by_id`, `test_unknown_product_returns_404` |
| TC-07 | Products | Search returns only matching products | API | `test_search_returns_only_matching_products` |
| TC-08 | Products | Search is case-insensitive | API | `test_search_is_case_insensitive` (3 variants) |
| TC-09 | Cart | Cart requires authentication | API | `test_cart_requires_authentication` |
| TC-10 | Cart | Add item to cart | API, smoke | `test_add_item_to_cart` |
| TC-11 | Cart | Total respects quantity | API | `test_cart_total_takes_quantity_into_account` |
| TC-12 | Cart | Total sums multiple products | API | `test_cart_total_sums_multiple_products` |
| TC-13 | Cart | Invalid quantity (0, -1, text) returns 400 | API | `test_invalid_quantity_is_rejected` (3 variants) |
| TC-14 | Cart | Quantity above stock returns 409 | API | `test_quantity_above_stock_returns_409` |
| TC-15 | Cart | Unknown product returns 404 | API | `test_adding_unknown_product_returns_404` |
| TC-16 | Checkout | Empty cart is rejected | API | `test_checkout_with_empty_cart_is_rejected` |
| TC-17 | Checkout | Address is required | API | `test_checkout_requires_address` |
| TC-18 | Checkout | Successful checkout creates order and empties cart | API, smoke | `test_successful_checkout_creates_order_and_empties_cart` |
| TC-19 | Login UI | Valid user lands on products page | UI, smoke | `test_valid_user_lands_on_products_page` |
| TC-20 | Login UI | Wrong password / locked user / empty form show messages | UI | `test_wrong_password_shows_error`, `test_locked_user_sees_lockout_message`, `test_empty_form_shows_required_message` |
| TC-21 | Login UI | Protected page redirects to login | UI | `test_products_page_redirects_to_login_when_logged_out` |
| TC-22 | Shop UI | Add to cart updates the counter | UI, smoke | `test_adding_a_product_updates_the_cart_counter` |
| TC-23 | Shop UI | Search filters, is case-insensitive, shows empty state | UI | `test_search_*` (3 tests) |
| TC-24 | Shop UI | Cart total reflects quantity | UI | `test_cart_total_reflects_quantity` |
| TC-25 | Shop UI | Remove item empties the cart | UI | `test_removing_an_item_empties_the_cart` |
| TC-26 | Shop UI | Checkout requires address | UI | `test_checkout_requires_address` |
| TC-27 | Shop UI | Complete purchase flow | UI, smoke | `test_complete_purchase_flow` |

Total: 38 automated test executions (parametrized variants counted individually).
