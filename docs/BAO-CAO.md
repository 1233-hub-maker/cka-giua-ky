# Báo cáo giữa kỳ CKA 2026 (tối đa 10 trang khi xuất PDF)
Nhóm: ... | Thành viên (5): ... | Repo: ...

## 1. Sơ đồ cluster
(vẽ: Trình duyệt -> NodePort 30080 -> Service frontend -> Pod frontend x2 -> Service backend -> Pod backend x2; cp, worker1, worker2, flannel)

## 2. Đóng gói Docker
- Dockerfile backend/frontend, lệnh build, push. Ảnh: Docker Hub có tag v1, v2.

## 3. Dựng cluster
- Cấu hình 3 VM (cloud, size, IP). Ảnh: `kubectl get nodes` 3 Ready.

## 4. Triển khai
- Ảnh: `kubectl get all -n demo-app -o wide`, trình duyệt truy cập app.

## 5. Vận hành
- 5.1 Scale 4 replicas (ảnh)  - 5.2 Update v2 + rollback (ảnh rollout history)
- 5.3 Tắt worker: quan sát + giải thích (xem README mục 4)

## 6. Khó khăn gặp phải và cách xử lý
