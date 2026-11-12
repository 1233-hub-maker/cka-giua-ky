# Bài tập giữa kỳ CKA 2026 – Docker + Kubernetes

Ứng dụng: frontend (nginx, proxy `/api/` sang backend) + backend (Node.js, trả về version, tên Pod, số lượt gọi).

```
app/backend   app/frontend   k8s/   docs/BAO-CAO.md
```

Thay `DOCKERHUB_USER` bằng tài khoản Docker Hub của nhóm:
```bash
sed -i 's/DOCKERHUB_USER/tenban/g' k8s/*.yaml
```

## 1. Docker
```bash
docker login
docker build -t tenban/demo-backend:v1  --build-arg APP_VERSION=v1 app/backend
docker build -t tenban/demo-frontend:v1 --build-arg APP_VERSION=v1 app/frontend
docker push tenban/demo-backend:v1
docker push tenban/demo-frontend:v1
```

## 2. Cluster (3 VM Ubuntu 22.04: cp, worker1, worker2)
Trên **cả 3 máy**:
```bash
sudo swapoff -a && sudo sed -i '/ swap / s/^/#/' /etc/fstab
printf "overlay\nbr_netfilter\n" | sudo tee /etc/modules-load.d/k8s.conf
sudo modprobe overlay br_netfilter
printf "net.bridge.bridge-nf-call-iptables=1\nnet.bridge.bridge-nf-call-ip6tables=1\nnet.ipv4.ip_forward=1\n" | sudo tee /etc/sysctl.d/k8s.conf
sudo sysctl --system
sudo apt-get update && sudo apt-get install -y containerd apt-transport-https ca-certificates curl gpg
sudo mkdir -p /etc/containerd && containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl restart containerd
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/k8s.gpg
echo "deb [signed-by=/etc/apt/keyrings/k8s.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /" | sudo tee /etc/apt/sources.list.d/k8s.list
sudo apt-get update && sudo apt-get install -y kubelet kubeadm kubectl && sudo apt-mark hold kubelet kubeadm kubectl
```
Trên **cp**:
```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
mkdir -p ~/.kube && sudo cp /etc/kubernetes/admin.conf ~/.kube/config && sudo chown $(id -u):$(id -g) ~/.kube/config
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```
Trên **worker1, worker2**: chạy lệnh `kubeadm join ...` do bước init in ra (sinh lại: `kubeadm token create --print-join-command`).
Mở firewall/security group: cp 6443; worker 30080 (NodePort) và 10250; UDP 8472 giữa các node (flannel).
```bash
kubectl get nodes     # 3 node Ready -> chụp ảnh
```

## 3. Triển khai
```bash
kubectl apply -f k8s/
kubectl get pods -n demo-app -o wide      # Pod nằm trên cả 2 worker
```
Truy cập: `http://<IP-public-worker>:30080`, bấm "Gọi backend" nhiều lần, thấy tên Pod thay đổi.

## 4. Vận hành
**Scale:**
```bash
kubectl scale deployment backend -n demo-app --replicas=4
kubectl get pods -n demo-app -o wide
```
**Cập nhật (v2) và rollback:**
```bash
docker build -t tenban/demo-backend:v2 --build-arg APP_VERSION=v2 app/backend && docker push tenban/demo-backend:v2
kubectl set image deployment/backend backend=tenban/demo-backend:v2 -n demo-app
kubectl rollout status deployment/backend -n demo-app
kubectl rollout history deployment/backend -n demo-app
kubectl rollout undo deployment/backend -n demo-app      # về v1
```
**Tắt một worker:**
```bash
# cửa sổ 1
kubectl get pods -n demo-app -o wide -w
# tắt (stop) VM worker2 trên cloud, cửa sổ 2:
kubectl get nodes -w
```
Giải thích (đưa vào báo cáo): sau ~40s không nhận heartbeat, node chuyển `NotReady`. Pod trên node đó bị Service loại khỏi danh sách endpoint ngay khi readiness fail nên người dùng vẫn được phục vụ bởi Pod ở worker còn lại (nhờ ≥2 replicas trải đều). Sau ~5 phút (`tolerationSeconds` mặc định 300 của taint `node.kubernetes.io/unreachable`) Pod bị evict (Terminating/Unknown), Deployment/ReplicaSet tạo Pod thay thế trên worker1. Bật lại node thì nó Ready lại, nhưng Pod **không tự chuyển ngược** về (scheduler không cân bằng lại).
