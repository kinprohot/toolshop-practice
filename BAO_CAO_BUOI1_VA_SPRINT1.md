# BÁO CÁO TIẾN ĐỘ BUỔI 1 & SPRINT 1 (AUTOMATION TESTING)

> **Thời gian thực hiện:** Ngày 10/11/2026  
> **Môi trường:** Windows 11, Python 3.12.6, Playwright 1.64.1, Pytest 9.2.0  
> **Repository thực hành:** [https://github.com/kinprohot/toolshop-practice](https://github.com/kinprohot/toolshop-practice) (Fork / Template từ `jameboykks/toolshop-practice`)  
> **Hệ thống kiểm thử mục tiêu:** Toolshop (`https://practicesoftwaretesting.com`)

---

## 1. TỔNG HỢP TIẾN ĐỘ THỰC HIỆN

| STT | Nhiệm vụ / Mục tiêu | Trạng thái | Ghi chú & Bằng chứng |
| :---: | :--- | :---: | :--- |
| **1** | Cài đặt môi trường máy tính (`doctor.py`) | **ĐÃ HOÀN THÀNH** | Máy đã sẵn sàng, 0 lỗi, 1 lưu ý (GitHub token). |
| **2** | Nhận bài giải Buổi 1 từ repo lớp (`lop/bai-giai`) | **ĐÃ HOÀN THÀNH** | Đã checkout `pages/` và `tests/buoi1/test_b1_pom.py` và commit. |
| **3** | Chạy kiểm thử Buổi 1 (`pytest tests/buoi1`) | **ĐÃ HOÀN THÀNH** | **13 passed** in 47.37s (100% bài đạt chuẩn). |
| **4** | Đọc tài liệu Buổi 1 (POM, Slide, Bài đọc) | **ĐÃ HOÀN THÀNH** | Đã nắm vững lý thuyết POM trong `bai-doc/buoi-1-page-object-model.md`. |
| **5** | Chuẩn bị khung kiểm thử cho Sprint 1 đồ án | **ĐÃ HOÀN THÀNH** | Đủ `conftest.py`, `pytest.ini`, `requirements.txt`, `.gitignore`, `.env.example`, `pages/`. |
| **6** | Viết 4 smoke test Sprint 1 (`tests/ui/test_smoke.py`) | **ĐÃ HOÀN THÀNH** | **4 passed** in 14.00s, tuân thủ 100% luật POM. |
| **7** | Tạo repo nhóm, thêm member, set branch protection | **CHƯA HOÀN THÀNH** | Cần thao tác trực tiếp trên giao diện GitHub của Trưởng nhóm. |
| **8** | Mở PR #1, bạn cùng nhóm Approve và Merge | **CHƯA HOÀN THÀNH** | Cần tài khoản của thành viên khác trong nhóm để Approve trên GitHub. |

---

## 2. CHI TIẾT CÁC TASK ĐÃ HOÀN THÀNH

### Task 1: Cài đặt & kiểm tra sức khoẻ môi trường (`doctor.py`)
- Môi trường ảo `.venv` được khởi tạo với Python 3.12.6.
- Đã cài đặt đầy đủ các gói trong `requirements.txt` và browser `playwright install chromium`.
- Đã sao chép `.env.example` thành `.env`.
- Chạy `python tools/doctor.py` cho kết quả:
  ```text
  Kiểm tra máy cho lớp Automation Testing (Windows 11)

  [OK]    Python 3.12.6
  [OK]    Đang dùng môi trường ảo
  [OK]    Đủ thư viện trong requirements.txt
  [OK]    BASE_URL = https://practicesoftwaretesting.com
  [OK]    API_URL = https://api.practicesoftwaretesting.com
  [OK]    API Toolshop trả lời (5.0)
  [OK]    Chromium mở được (phiên bản 156.0.8078.4)
  [OK]    Trang chủ Toolshop hiện 9 sản phẩm
  [LƯU Ý] GitHub API: còn 51/60 lượt gọi trong giờ này (chưa có token)
          -> Cả lớp chung một IP chỉ có 60 lượt/giờ. Nên tạo token cho buổi 2.
  [OK]    Git: git version 2.55.0.windows.5, tên 'Nontew_023'
  [OK]    Node.js v20.18.0 (cần cho Playwright MCP, buổi 4)

  0 lỗi, 1 lưu ý. Máy đã sẵn sàng.
  ```

---

### Task 2 & 3: Nhận bài giải Buổi 1 và xác minh 13 test Buổi 1
- Đã cấu hình remote lớp: `git remote add lop https://github.com/jameboykks/toolshop-practice.git`.
- Lấy bài giải chuẩn: `git checkout lop/bai-giai -- pages tests/buoi1/test_b1_pom.py`.
- Commit bài giải: `git commit -m "Take the session 1 reference solution"`.
- Thực hiện chạy `pytest tests/buoi1`:
  ```text
  collected 13 items

  tests\buoi1\test_b1_pom.py .........                                     [ 69%]
  tests\buoi1\test_b1_spaghetti.py ....                                    [100%]

  ============================= 13 passed in 47.37s =============================
  ```
- **Kết quả:** Đạt chính xác **13/13 test passed** bao gồm 9 test POM và 4 test mẫu spaghetti.

---

### Task 4: Nắm vững lý thuyết Buổi 1 (Page Object Model)
- Đã đối chiếu tài liệu `bai-doc/buoi-1-page-object-model.md` và các quy tắc:
  1. **Quy tắc phân tách:** Locator chỉ nằm trong `pages/`. Assertion (`expect`, `assert`) chỉ nằm trong `tests/`.
  2. **Quy tắc chờ:** Tuyệt đối không dùng `time.sleep()` hoặc `wait_for_timeout()`. Chỉ dùng auto-waiting của Playwright (`expect()`).
  3. **Quy tắc docstring:** Mỗi hàm kiểm thử phải có docstring 3 dòng (Goal, Precondition, Expected).
  4. **An toàn tài khoản:** Tuyệt đối không thử đăng nhập sai với tài khoản mẫu `customer@practicesoftwaretesting.com` để tránh khoá tài khoản dùng chung của cả lớp.

---

### Task 5 & 6: Viết 4 smoke test cho Sprint 1 đồ án
Đã tạo file `tests/ui/test_smoke.py` và cập nhật `pages/contact_page.py` với các thuộc tính locator lỗi rõ ràng (`self.subject_error`, `self.message_error`).

Nội dung 4 bài test đáp ứng chính xác bảng yêu cầu trong `docs/sprint-1.md`:
1. **Test 1 - Tìm kiếm:** Mở trang chủ, tìm `"pliers"` -> caption chứa chữ "pliers", tất cả tên sản phẩm trả về đều chứa "pliers".
2. **Test 2 - Thêm vào giỏ:** Mở sản phẩm `"Claw Hammer"`, chọn số lượng 3 và bấm Add to cart -> toast hiện thông báo, badge giỏ hàng trên header hiện `"3"`.
3. **Test 3 - Đăng nhập sai:** Dùng email ngẫu nhiên không tồn tại (`nobody-exists-sprint1@example.com`) và mật khẩu bất kỳ -> thông báo lỗi `"Invalid email or password"`, URL vẫn giữ nguyên ở `/auth/login`. (Đảm bảo an toàn, không đụng vào `customer@practicesoftwaretesting.com`).
4. **Test 4 - Form liên hệ trống:** Mở trang `/contact`, không điền gì và bấm Send -> xuất hiện lỗi `"Subject is required"` và `"Message is required"`.

#### Bằng chứng kiểm tra vi phạm quy tắc (Phải không có output):
```powershell
Select-String -Path tests\ui\*.py -Pattern "get_by_|locator\("
Select-String -Path pages\*.py -Pattern "expect\(|assert "
Select-String -Path tests\ui\*.py,pages\*.py -Pattern "sleep|wait_for_timeout"
```
-> Kết quả: Cả 3 lệnh đều không in ra bất kỳ dòng nào (0 vi phạm, tuân thủ 100%).

#### Bằng chứng chạy kiểm thử 4 smoke test:
```text
pytest tests/ui/test_smoke.py -m smoke

collected 4 items

tests\ui\test_smoke.py ....                                              [100%]

============================= 4 passed in 14.00s ==============================
```
- Toàn bộ code đã được commit và push lên nhánh `main` của repo cá nhân: `kinprohot/toolshop-practice`.

---

## 3. CÁC TASK CHƯA THỰC HIỆN ĐƯỢC VÀ LÝ DO CỤ THỂ

### 1. Task C.1: Tạo repo nhóm trên GitHub, thêm thành viên và thiết lập Branch Protection Rule
- **Trạng thái:** Chưa thực hiện trên GitHub.
- **Lý do khách quan 100%:**
  - Repo nhóm (`toolshop-automation-<tên nhóm>`) bắt buộc phải do Trưởng nhóm tạo trên giao diện GitHub Web.
  - Thao tác mời thành viên nhóm (`Settings` -> `Collaborators` -> `Add people`) và cấu hình luật bảo vệ nhánh `main` (`Settings` -> `Branches` -> `Require pull request before merging` -> `Require approvals: 1`) đòi hỏi quyền sở hữu tài khoản GitHub của nhóm sinh viên trên trình duyệt.
- **Cách giải quyết:** Xem hướng dẫn từng bước ở Mục 4 bên dưới.

### 2. Task C.4: Mở PR #1, nhờ bạn trong nhóm Review & Approve rồi mới Merge
- **Trạng thái:** Chưa thực hiện trên GitHub.
- **Lý do khách quan 100%:**
  - Theo chính sách phân quyền của GitHub, người mở Pull Request **không được phép tự Approve PR của chính mình**.
  - Bắt buộc phải có một bạn khác trong nhóm đăng nhập tài khoản GitHub cá nhân, mở tab **Files changed**, chọn **Review changes** -> **Approve** -> **Submit review**. Sau khi xuất hiện dấu tick xanh Approved thì người tạo PR mới bấm **Merge pull request**.
- **Cách giải quyết:** Toàn bộ code của PR #1 (khung kiểm thử + 4 test smoke) đã được code và kiểm thử thành công sẵn sàng. Nhóm chỉ cần đẩy lên nhánh `feature/...` và thao tác mở/review PR.

### 3. Task tài liệu PDF Google Drive (Slide, Bài đọc, Phiếu thực hành)
- **Trạng thái:** Các link Google Drive cần sinh viên đăng nhập trình duyệt để tải/đọc trực tiếp.
- **Lý do:** Đây là tài liệu đọc tham khảo cá nhân. Toàn bộ nội dung lý thuyết và phiếu bài tập cốt lõi đã có đầy đủ dưới dạng Markdown ngay trong repo tại `bai-doc/buoi-1-page-object-model.md` và `docs/sprint-1.md`.

---

## 4. HƯỚNG DẪN 5 BƯỚC HOÀN THÀNH NỐT ĐỒ ÁN SPRINT 1 TRƯỚC BUỔI 11/11

### Bước 1: Trưởng nhóm tạo repo nhóm và thiết lập Branch Protection (5 phút)
1. Truy cập GitHub cá nhân -> Bấm nút **New** (Repository).
2. Đặt tên: `toolshop-automation-<tên-nhóm>`, chọn **Public**, tích chọn **Add a README file** -> Bấm **Create repository**.
3. Vào **Settings** -> **Collaborators** -> **Add people**: Nhập username GitHub của các thành viên trong nhóm. Các thành viên vào email hoặc thông báo GitHub để bấm **Accept invitation**.
4. Vào **Settings** -> **Branches** -> Bấm **Add classic branch protection rule**:
   - **Branch name pattern:** điền `main`
   - Tích chọn: **Require a pull request before merging**
   - Ở mục **Require approvals:** chọn `1`
   - Bấm **Create** (nhập mật khẩu GitHub nếu được hỏi).

### Bước 2: Clone repo nhóm về và tạo nhánh tính năng
```bash
git clone https://github.com/<truong-nhom>/toolshop-automation-<ten-nhom>.git
cd toolshop-automation-<ten-nhom>
git checkout -b feature/sprint1-framework-and-smoke
```

### Bước 3: Chép các file đã chuẩn bị sẵn từ repo `toolshop-practice` sang repo nhóm
Chép nguyên vẹn các file và thư mục sau từ `C:\Users\Maryeel\Desktop\CuoiKyTesting\toolshop-practice` sang thư mục repo nhóm:
- `conftest.py`
- `pytest.ini`
- `requirements.txt`
- `.gitignore`
- `.env.example`
- Thư mục `pages/` (gồm 7 page objects)
- Thư mục `tests/ui/test_smoke.py` (chứa 4 test smoke đã pass)

Kiểm tra bằng cách tạo file `.env` và chạy test trong repo nhóm:
```powershell
copy .env.example .env
pytest tests/ui/test_smoke.py -m smoke
```
*(Kết quả chắc chắn sẽ ra `4 passed` như đã xác minh).*

### Bước 4: Commit và đẩy nhánh lên GitHub
```powershell
git add conftest.py pytest.ini requirements.txt .gitignore .env.example pages tests
git status   # Chắc chắn không có tệp .env trong danh sách commit!
git commit -m "Add test framework and 4 smoke tests"
git push -u origin feature/sprint1-framework-and-smoke
```

### Bước 5: Mở Pull Request & Nhờ thành viên Review
1. Trên GitHub repo nhóm, bấm **Compare & pull request**.
2. **Tiêu đề:** `Sprint 1: framework and smoke tests`.
3. **Mô tả:** Dán kết quả chạy `4 passed in 14.00s`.
4. Ở cột bên phải mục **Reviewers**: Chọn 1 bạn trong nhóm. Bấm **Create pull request**.
5. Bạn reviewer mở PR -> Vào tab **Files changed** -> Bấm nút **Review changes** -> Chọn **Approve** -> Bấm **Submit review**.
6. Người mở PR bấm nút **Merge pull request** -> **Confirm merge**.

---

## 5. KỊCH BẢN CHIẾU 1 PHÚT NGHIỆM THU ĐẦU BUỔI 11/11
Khi giảng viên gọi nhóm lên chiếu màn hình:
1. **Màn hình 1 (20 giây):** Mở GitHub repo nhóm -> Vào **Settings** -> **Branches**: Chiếu dòng luật bảo vệ nhánh `main` (`Require pull request before merging`, `1 approval`).
2. **Màn hình 2 (20 giây):** Vào tab **Pull requests** -> Bấm mục **Closed**: Mở PR #1 đã merge, chỉ rõ dấu tick xanh **Approved** của bạn cùng nhóm.
3. **Màn hình 3 (20 giây):** Mở terminal gõ:
   ```powershell
   pytest tests/ui/test_smoke.py -m smoke
   ```
   Show dòng kết quả màu xanh lá: `4 passed`.
