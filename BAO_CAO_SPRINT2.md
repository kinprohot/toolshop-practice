# BÁO CÁO TIẾN ĐỘ SPRINT 2 (NỬA ĐẦU - HẠN 18/11)

> **Repository:** [https://github.com/kinprohot/toolshop-practice](https://github.com/kinprohot/toolshop-practice)  
> **Nhánh phát triển:** `feature/luc-sprint2`  
> **Tác giả:** Nontew_023 (`lucnguyen0232003@gmail.com`)  
> **Trạng thái:** Đã hoàn thành 100% các tiêu chí và đã push lên GitHub.

---

## 1. TỔNG HỢP KẾT QUẢ KIỂM THỬ SPRINT 2

| Mục yêu cầu (docs/sprint-2.md) | Chỉ tiêu tối thiểu | Kết quả thực tế đạt được | Trạng thái |
|---|:---:|:---:|:---:|
| **Test API** | ≥ 5 test API | **10 test API** (GET/POST, 4xx, token, contract, cart) | **ĐẠT (Vượt chỉ tiêu)** |
| **Phương thức HTTP** | ≥ 2 phương thức | GET và POST | **ĐẠT** |
| **Test lỗi 4xx** | ≥ 1 test lỗi 4xx | 3 test (401, 404, 422) | **ĐẠT** |
| **Test cấu trúc JSON** | ≥ 1 test contract | Test cấu trúc phân trang và sản phẩm của `/products` | **ĐẠT** |
| **Test có token xác thực** | ≥ 1 test có token | Test `/users/me` với Bearer token | **ĐẠT** |
| **Test Route / Mocking** | 2 test route | 2 test (chặn ảnh + mock danh sách rỗng) | **ĐẠT** |
| **Test Parametrize** | 2 test (1 đọc file) | 2 test: đọc `search_keywords.json` + test lỗi 4xx | **ĐẠT** |
| **Test Giao diện (UI)** | ≥ 12 test, ≥ 8 xanh | **15 test UI (100% xanh)** phủ đủ 6 nhóm chức năng | **ĐẠT (Vượt chỉ tiêu)** |
| **Dùng fixture `logged_in_page`** | ≥ 1 test | 1 test trang tài khoản dùng storage_state | **ĐẠT** |
| **Kiểm tra luật POM & Playwright** | 0 vi phạm | Không sleep, không locator trong test, không assert trong pages | **ĐẠT 100%** |

---

## 2. CHI TIẾT CẤU TRÚC TỆP SPRINT 2 ĐÃ TẠO

### A. Nhóm kiểm thử API (`tests/api/`) - 10 passed in 11.12s
- **`tests/api/test_products_api.py`**:
  - `test_products_first_page_has_pagination_and_product_shape`: Kiểm tra hợp đồng API GET `/products` (keys phân trang, kiểu dữ liệu id, name, price > 0, không so số lượng tuyệt đối).
  - `test_products_search_api_returns_only_matching_names`: Data-driven test đọc bộ từ khóa từ `data/search_keywords.json` (`pliers`, `hammer`, `saw`, `wrench`).
  - `test_products_protected_or_missing_resource_returns_4xx`: Parametrize kiểm tra lỗi 401 (`/users/me`) và 404 (`/products/does-not-exist`).
- **`tests/api/test_users_api.py`**:
  - `test_users_register_empty_body_returns_422_with_field_errors`: Kiểm tra validation server-side trả về lỗi 422 với body rỗng.
  - `test_users_me_with_token_returns_own_profile`: Kiểm tra xác thực Bearer token trả về đúng thông tin tài khoản vừa đăng ký.
- **`tests/api/test_carts_api.py`**:
  - `test_cart_add_product_quantity_two_is_stored`: Sử dụng fixture `new_cart` (POST `/carts`) và kiểm tra lưu sản phẩm số lượng 2 vào giỏ (POST & GET).

### B. Nhóm kiểm thử Route / Mocking (`tests/ui/test_network.py`) - 2 passed
- `test_network_home_without_images_still_lists_products`: Dùng `page.route` chặn các file ảnh (.png, .jpg...) và xác minh trang web vẫn hiển thị danh sách sản phẩm.
- `test_network_home_with_empty_product_list_shows_no_results`: Dùng `page.route` giả lập API `/products` trả về 0 sản phẩm để kiểm tra hiển thị thông báo rỗng *"There are no products found."*.

### C. Nhóm kiểm thử Giao diện (`tests/ui/`) - 15 passed in 49.69s
Bao phủ toàn bộ 6 nhóm chức năng của hệ thống:
1. **Danh sách & Tìm kiếm:**
   - `test_smoke_search_keyword_shows_matching_products` (Tìm "pliers")
   - `test_search_unknown_keyword_shows_no_results` (Tìm từ khóa không tồn tại)
   - `test_sort_by_price_orders_products` (Sắp xếp theo giá tăng dần và giảm dần)
2. **Bộ lọc:**
   - `test_filter_by_category_hammer_shows_matching_products` (Lọc theo danh mục Hammer)
3. **Chi tiết sản phẩm:**
   - `test_smoke_product_add_quantity_three_updates_cart_badge` (Thêm số lượng 3)
   - `test_product_detail_shows_correct_name_and_price` (Hiển thị tên và đơn giá)
4. **Giỏ hàng:**
   - `test_cart_line_price_equals_unit_price_times_quantity` (Thành tiền = đơn giá x số lượng)
   - `test_cart_continue_shopping_returns_to_home` (Bấm tiếp tục mua sắm quay lại trang chủ)
5. **Xác thực:**
   - `test_smoke_login_wrong_password_shows_error` (Đăng nhập sai tài khoản)
   - `test_login_empty_form_shows_required_errors` (Để trống form đăng nhập)
6. **Liên hệ & Tài khoản:**
   - `test_smoke_contact_empty_form_shows_required_errors` (Để trống form liên hệ)
   - `test_account_page_logged_in_shows_user_menu` (Dùng `logged_in_page` với session storage_state vào trang My account)

---

## 3. BẰNG CHỨNG KIỂM TRA LUẬT & KẾT QUẢ CHẠY TEST

### Kiểm tra không vi phạm quy tắc:
```powershell
Select-String -Path tests\api\*.py,tests\ui\*.py -Pattern "import requests"
Select-String -Path tests\api\*.py,tests\ui\*.py -Pattern "get_by_|locator\("
Select-String -Path pages\*.py -Pattern "expect\(|assert "
Select-String -Path tests\api\*.py,tests\ui\*.py,pages\*.py -Pattern "sleep|wait_for_timeout"
```
👉 **Kết quả:** Không có dòng nào xuất hiện (0 vi phạm).

### Chạy kiểm thử:
- `pytest tests/api` $\rightarrow$ **10 passed in 11.12s**
- `pytest tests/ui` $\rightarrow$ **15 passed in 49.69s**
- `pytest -m smoke` $\rightarrow$ **4 passed**
- `pytest -m api` $\rightarrow$ **10 passed**
