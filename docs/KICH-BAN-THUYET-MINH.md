# Kịch bản thuyết minh (8–10 phút), khớp với video demo

Đọc theo từng đoạn tương ứng với từng bước trong video.

**0. Mở đầu (~30s)**
Chào thầy cô và các bạn. Nhóm em triển khai một ứng dụng web gồm frontend và backend lên Kubernetes. Cluster gồm 1 control plane và 2 worker trên Azure, dựng bằng kubeadm.

**1. Docker Hub (~30s)**
Hai thành phần được đóng gói bằng Docker và đẩy lên Docker Hub: `demo-backend` có tag v1, v2 và `demo-frontend` có tag v1. Nhóm gắn tag phiên bản, không dùng `latest`, để biết chính xác mỗi Pod đang chạy phiên bản nào.

**2. Mã nguồn (~30s)**
Mỗi thành phần có một Dockerfile riêng. Thư mục `k8s` chứa 3 file YAML: namespace, deployment và service của backend, deployment và service của frontend. Toàn bộ tạo bằng `kubectl apply`.

**3. Cluster (~30s)**
Lệnh `kubectl get nodes` cho thấy 3 node `cp`, `worker1`, `worker2` đều ở trạng thái Ready. Mạng Pod dùng plugin CNI flannel.

**4. Triển khai (~45s)**
Ứng dụng chạy trong namespace riêng `demo-app`. Mỗi Deployment có 2 replicas, được dàn đều lên cả 2 worker nhờ `topologySpreadConstraints`. Frontend gọi backend qua Service `backend` bằng tên DNS nội bộ, còn người dùng truy cập từ ngoài qua Service NodePort cổng 30080.

**5. Truy cập ứng dụng (~45s)**
Em mở trình duyệt tại IP worker1, cổng 30080 và bấm "Gọi backend". Tên Pod thay đổi giữa các lần bấm, chứng tỏ Service đang chia tải cho 2 Pod backend. Truy cập qua IP worker2 cũng được vì NodePort mở trên mọi node.

**6. Scale (~45s)**
Em scale backend từ 2 lên 4 replicas bằng một lệnh. Kubernetes ghi nhận yêu cầu, tạo thêm 2 Pod mới và lập lịch lên các worker. Số Pod luôn bám theo con số em đặt.

**7. Cập nhật v2 (~60s)**
Em đổi image của backend sang v2. Kubernetes thực hiện rolling update: tạo Pod mới trước rồi xóa Pod cũ dần dần nên ứng dụng không bị gián đoạn. Trên trình duyệt, kết quả đã đổi sang `version: v2`. Frontend không đổi nên vẫn là v1.

**8. Rollback (~60s)**
Giả sử bản v2 có lỗi, em dùng `rollout undo` để quay về bản trước. Kubernetes giữ lịch sử các lần cập nhật nên việc quay lại rất nhanh. Có thể thấy các Pod v2 đang `Terminating` trong khi Pod v1 mới được tạo. Kết quả trên trình duyệt trở lại `v1`.

**9. Tắt worker (~2 phút)**
Em dừng máy ảo worker2 trên Azure.
- Sau khoảng 40 giây, node chuyển sang `NotReady` vì không còn nhận được tín hiệu từ kubelet.
- Ngay lúc đó Service loại các Pod ở worker2 ra khỏi danh sách phục vụ, nên ứng dụng vẫn chạy bình thường nhờ Pod ở worker1. Đây là lý do cần ít nhất 2 replicas trên 2 worker khác nhau.
- Sau khoảng 5 phút, Kubernetes coi node đã mất, xóa các Pod ở worker2 và tạo Pod thay thế trên worker1 để giữ đúng số replicas.
- Khi bật lại worker2, Pod không tự chuyển ngược về, vì Kubernetes không tự cân bằng lại các Pod đang chạy.

**10. Kết (~45s)**
Khó khăn chính: hạn mức Azure for Students nên phải dùng lại các máy ảo sẵn có, thiếu `conntrack` khi chạy kubeadm trên Ubuntu 24.04, và Pod bị dồn về một worker sau khi giảm số replicas. Nhóm đã xử lý các vấn đề này và hoàn thành đầy đủ yêu cầu của đề. Em xin cảm ơn.

## Câu hỏi thường gặp khi vấn đáp
- **Pod là gì?** Đơn vị nhỏ nhất Kubernetes quản lý, bọc một hoặc nhiều container. Ở bài này mỗi Pod có một container.
- **Deployment và ReplicaSet khác gì?** Deployment quản lý phiên bản và cập nhật. ReplicaSet giữ đủ số Pod cho một phiên bản.
- **Vì sao dùng Service?** Pod có IP thay đổi liên tục. Service cho một địa chỉ ổn định và chia tải đến các Pod.
- **NodePort là gì?** Mở một cổng (30080) trên mọi node để truy cập từ bên ngoài.
- **Scale tự động không?** Bài này scale thủ công. Scale tự động theo tải cần HPA.
- **Vì sao Pod không chuyển ngược lại sau khi bật node?** Scheduler chỉ đặt Pod lúc tạo, không di chuyển Pod đang chạy.
