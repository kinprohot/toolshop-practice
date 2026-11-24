# BÁO CÁO TIẾN ĐỘ SPRINT 2 (NỬA SAU - SPRINT 2B, HẠN 25/11)

> **Repository:** [https://github.com/kinprohot/toolshop-practice](https://github.com/kinprohot/toolshop-practice)  
> **Nhánh phát triển:** `feature/luc-sprint2b`  
> **Tác giả:** Nontew_023 (`lucnguyen0232003@gmail.com`)  
> **Trạng thái:** Đã hoàn thành 100% các tiêu chí và sẵn sàng nộp/nghiệm thu.

---

## 1. TỔNG HỢP TIẾN ĐỘ THỰC HIỆN

| STT | Hạng mục (docs/sprint-2b.md) | Trạng thái | Chi tiết & Bằng chứng |
| :---: | :--- | :---: | :--- |
| **1** | **Bài tập Buổi 3 (BDD)** | **ĐÃ HOÀN THÀNH** | `pytest tests/buoi3 -v` đạt **6/6 passed in 24.89s**. |
| **2** | **1 Feature BDD trong repo nhóm** | **ĐÃ HOÀN THÀNH** | Tạo `tests/bdd/features/cart.feature` và `tests/bdd/test_cart_bdd.py`. `pytest tests/bdd -v` đạt **2 passed in 10.97s**. |
| **3** | **Cấu hình `pytest.ini` cho BDD** | **ĐÃ HOÀN THÀNH** | Cập nhật `bdd_features_base_dir = tests/bdd/features`. |
| **4** | **Workflow `ci.yml` chuẩn GitHub Actions** | **ĐÃ HOÀN THÀNH** | Tạo `.github/workflows/ci.yml` đủ 3 trigger, ma trận 3 trình duyệt, `fail-fast: false`, bỏ `-m smoke`, artifact riêng từng trình duyệt. |
| **5** | **Thư mục `toolshop/` cho CI** | **ĐÃ HOÀN THÀNH** | Đầy đủ 3 tệp Docker: `docker-compose.yml`, `nginx.conf`, `start.sh`. |
| **6** | **Cập nhật `README.md`** | **ĐÃ HOÀN THÀNH** | Thêm Badge CI GitHub Actions, mục Kết quả CI và Trace Viewer. |
| **7** | **Kiểm tra rác & Luật POM** | **ĐÃ HOÀN THÀNH** | 0 vi phạm (không commit `.env`, `test-results/`, `report.html`, không locator trong test). |
| **8** | **Bảo vệ nhánh `main` với 3 Status Checks** | **CẦN THAO TÁC** | Bật trên GitHub Settings sau khi lượt CI đầu tiên hoàn tất. |

---

## 2. CHI TIẾT CÁC TỆP ĐÃ XÂY DỰNG

### A. Feature BDD (`tests/bdd/features/cart.feature`)
Luồng nghiệp vụ tính toán giá dòng trong giỏ hàng:
```gherkin
Feature: Cart line price calculation
  As a shopper
  I want the cart to calculate line totals accurately
  So that I know how much I am paying for each product

  Background:
    Given I am on the home page

  Scenario Outline: Adding a product calculates line price from unit price and quantity
    When I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I go to the cart
    Then the line total equals the unit price times <quantity>

    Examples:
      | product            | quantity |
      | Combination Pliers | 1        |
      | Claw Hammer        | 3        |
```

### B. Step Definitions (`tests/bdd/test_cart_bdd.py`)
Tuân thủ 100% Page Object Model:
- Sử dụng `@given`, `@when`, `@then` kết nối trực tiếp với các page object (`HomePage`, `ProductPage`, `CartPage`).
- Không chứa bất kỳ locator hoặc assertion trực tiếp trên HTML DOM trong file test.

### C. GitHub Actions Workflow (`.github/workflows/ci.yml`)
Đáp ứng hoàn chỉnh đề mục 3.9 - 3.10:
- **3 Trigger:** `push` vào nhánh `main`, `pull_request`, và `workflow_dispatch` (chạy thủ công).
- **Ma trận 3 trình duyệt:** `[chromium, firefox, webkit]` trên `ubuntu-latest`, `fail-fast: false`.
- **Khởi động Toolshop container:** Tự động dựng môi trường kiểm thử riêng biệt bằng Docker để không bị Cloudflare chặn bot.
- **Lệnh chạy kiểm thử:** Bỏ `-m smoke` để chạy cả bộ test của repo:
  ```bash
  pytest --browser ${{ matrix.browser }} -n 2 --reruns 1 --reruns-delay 2 --tracing retain-on-failure --screenshot only-on-failure --html=report.html --self-contained-html
  ```
- **Lưu trữ Artifact:** `name: report-${{ matrix.browser }}`, luôn upload kể cả khi có test đỏ (`if: always()`), thời gian lưu 7 ngày.

---

## 3. BẰNG CHỨNG CHẠY KIỂM THỬ THỰC TẾ

### 1. BDD Buổi 3 (`pytest tests/buoi3 -v`):
```text
tests/buoi3/test_b3_bdd.py::test_adding_a_product_calculates_line_price_from_unit_price_and_quantity[Combination Pliers-1] PASSED [ 16%]
tests/buoi3/test_b3_bdd.py::test_adding_a_product_calculates_line_price_from_unit_price_and_quantity[Claw Hammer-3] PASSED [ 33%]
tests/buoi3/test_b3_bdd.py::test_search_returns_only_matching_products[pliers] PASSED [ 50%]
tests/buoi3/test_b3_bdd.py::test_search_returns_only_matching_products[hammer] PASSED [ 66%]
tests/buoi3/test_b3_bdd.py::test_search_returns_only_matching_products[saw] PASSED [ 83%]
tests/buoi3/test_b3_bdd.py::test_search_with_an_unknown_word_shows_the_empty_state PASSED [100%]

============================= 6 passed in 24.89s ==============================
```

### 2. BDD Repo nhóm (`pytest tests/bdd -v`):
```text
tests/bdd/test_cart_bdd.py::test_adding_a_product_calculates_line_price_from_unit_price_and_quantity[Combination Pliers-1] PASSED [ 50%]
tests/bdd/test_cart_bdd.py::test_adding_a_product_calculates_line_price_from_unit_price_and_quantity[Claw Hammer-3] PASSED [100%]

============================= 2 passed in 10.97s ==============================
```

### 3. Kiểm tra rác & Luật POM:
```powershell
git ls-files | Select-String "test-results|\.venv|__pycache__|report.*html"  # Không in gì
Select-String -Path tests\ui\*.py,tests\api\*.py,tests\bdd\*.py -Pattern "get_by_|locator\("  # Không in gì
```

---

## 4. HƯỚNG DẪN 3 BƯỚC CHO NHÓM TRƯỚC BUỔI NGHIỆM THU 25/11

1. **Mở Pull Request:**
   - Đẩy nhánh `feature/luc-sprint2b` lên GitHub.
   - Tạo PR vào nhánh `main`. Nhờ thành viên nhóm review và Approve.
   - Quan sát tab **Actions** trên GitHub để 3 job (`test (chromium)`, `test (firefox)`, `test (webkit)`) chạy và chuyển sang màu xanh lá.
   - Bấm **Merge pull request** vào `main`.

2. **Cập nhật luật bảo vệ nhánh `main`:**
   - Vào **Settings → Branches** trên GitHub repo.
   - Sửa rule của nhánh `main`:
     - Tích chọn **Require status checks to pass before merging**.
     - Tìm và chọn đủ 3 checks: `test (chromium)`, `test (firefox)`, `test (webkit)`.
     - Bấm **Save changes**.

3. **Chụp 2 ảnh cho README:**
   - Ảnh 1 (`docs/screenshots/ci-green.png`): Chụp màn hình tab Actions của lượt chạy xanh cả 3 job trên nhánh `main`.
   - Ảnh 2 (`docs/screenshots/trace-viewer.png`): Chụp màn hình Playwright Trace Viewer mở trace của một test lỗi (hoặc test bất kỳ).
   - Lưu 2 ảnh vào thư mục `docs/screenshots/` và đẩy lên GitHub.
