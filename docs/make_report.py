from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Preformatted, Table, TableStyle, Flowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("A", F + r"\arial.ttf"))
pdfmetrics.registerFont(TTFont("AB", F + r"\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("C", F + r"\consola.ttf"))

B = ParagraphStyle("b", fontName="A", fontSize=10.5, leading=15, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="AB", fontSize=15, leading=19, spaceBefore=8, spaceAfter=8,
                    textColor=colors.HexColor("#1a3c6e"))
H2 = ParagraphStyle("h2", fontName="AB", fontSize=11.5, leading=15, spaceBefore=6, spaceAfter=4)
T = ParagraphStyle("t", fontName="AB", fontSize=20, leading=26, alignment=1, spaceAfter=10)
CODE = ParagraphStyle("c", fontName="C", fontSize=8.5, leading=11,
                      backColor=colors.HexColor("#f0f0f0"), borderPadding=4, spaceAfter=8)


class Shot(Flowable):
    """Khung trống để dán ảnh chụp màn hình."""

    def __init__(s, caption, h=5.2 * cm):
        super().__init__()
        s.c, s.h = caption, h

    def wrap(s, aw, ah):
        s.w = aw
        return aw, s.h + 0.7 * cm

    def draw(s):
        c = s.canv
        c.setStrokeColor(colors.grey)
        c.setDash(4, 3)
        c.rect(0, 0.6 * cm, s.w, s.h)
        c.setDash()
        c.setFont("A", 9)
        c.setFillColor(colors.grey)
        c.drawCentredString(s.w / 2, 0.6 * cm + s.h / 2, "[ Dán ảnh chụp màn hình vào đây ]")
        c.setFillColor(colors.black)
        c.drawString(0, 0.1 * cm, "Hình: " + s.c)


import os
from reportlab.platypus import Image, KeepTogether
from reportlab.lib.utils import ImageReader


def shot(n, caption, h=5.2 * cm):
    """Dùng docs/images/<n>.png (hoặc .jpg) nếu có, nếu không thì để khung trống."""
    for ext in ("png", "jpg", "jpeg"):
        path = os.path.join("docs", "images", "%s.%s" % (n, ext))
        if os.path.exists(path):
            iw, ih = ImageReader(path).getSize()
            maxw, maxh = 16.5 * cm, max(h * 1.5, 6 * cm)
            k = min(maxw / iw, maxh / ih)
            return KeepTogether([Image(path, iw * k, ih * k),
                                 Paragraph("<i>Hình: %s</i>" % caption,
                                           ParagraphStyle("cap", fontName="A", fontSize=9, spaceAfter=8))])
    return Shot(caption, h)


class Diagram(Flowable):
    def wrap(s, aw, ah):
        s.w = aw
        return aw, 9.5 * cm

    def draw(s):
        c = s.canv
        W = s.w

        def box(x, y, w, h, t, fill="#dbe9ff", sub=None):
            c.setFillColor(colors.HexColor(fill))
            c.setStrokeColor(colors.HexColor("#1a3c6e"))
            c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
            c.setFillColor(colors.black)
            c.setFont("AB", 8.5)
            c.drawCentredString(x + w / 2, y + h - 12, t)
            if sub:
                c.setFont("A", 7.5)
                c.drawCentredString(x + w / 2, y + h - 23, sub)

        def line(x1, y1, x2, y2):
            c.setStrokeColor(colors.HexColor("#444"))
            c.line(x1, y1, x2, y2)

        box(W / 2 - 60, 8.3 * cm, 120, 28, "Trình duyệt", "#fff3cd", "http://IP-worker:30080")
        box(W / 2 - 95, 6.3 * cm, 190, 28, "Service frontend (NodePort 30080)", "#e2f0d9")
        line(W / 2, 8.3 * cm, W / 2, 6.3 * cm + 28)
        box(5, 0.2 * cm, W / 3 - 10, 5.3 * cm, "cp (control plane)", "#f4f4f4", "kubeadm, flannel")
        box(W / 3 + 5, 0.2 * cm, W / 3 - 10, 5.3 * cm, "worker1", "#f4f4f4")
        box(2 * W / 3 + 5, 0.2 * cm, W / 3 - 10, 5.3 * cm, "worker2", "#f4f4f4")
        for x0 in (W / 3 + 15, 2 * W / 3 + 15):
            box(x0, 3.1 * cm, W / 3 - 30, 24, "Pod frontend", "#c6e0b4")
            box(x0, 1.0 * cm, W / 3 - 30, 24, "Pod backend", "#f8cbad")
            line(W / 2, 6.3 * cm, x0 + (W / 3 - 30) / 2, 3.1 * cm + 24)
        c.setFont("A", 7.5)
        c.setFillColor(colors.HexColor("#444"))
        c.drawCentredString(W / 2, 5.85 * cm, "frontend gọi backend qua Service backend (ClusterIP:3000)")
        box(15, 3.1 * cm, W / 3 - 30, 24, "API server, etcd", "#e8e8e8")


def P(t, s=B):
    return Paragraph(t, s)


def code(t):
    return Preformatted(t, CODE)


story = []
story += [
    Spacer(1, 3 * cm), P("BÁO CÁO BÀI TẬP GIỮA KỲ – KHOÁ CKA 2026", T),
    P("Triển khai ứng dụng web với Docker và Kubernetes",
      ParagraphStyle("s", parent=B, alignment=1, fontSize=13)),
    Spacer(1, 1 * cm),
    P("Nhóm: ……………………………&nbsp;&nbsp;&nbsp;Thành viên (5 sinh viên): ………………………………"),
    P("Repository Git: ……………………………………………"),
    P("Docker Hub: <b>dami1705/demo-backend</b>, <b>dami1705/demo-frontend</b> (tag v1, v2)"),
    P("Ngày nộp: 19/11/2026"), PageBreak()]

story += [
    P("1. Tổng quan và sơ đồ cluster", H1),
    P("Ứng dụng demo gồm <b>frontend</b> (nginx phục vụ trang HTML và chuyển tiếp đường dẫn <i>/api/</i>) và "
      "<b>backend</b> (Node.js, trả về phiên bản, tên Pod và số lượt gọi). Cả hai được đóng gói bằng Docker, "
      "đẩy lên Docker Hub và triển khai lên cluster Kubernetes dựng bằng kubeadm gồm 1 control plane và "
      "2 worker trên Microsoft Azure."),
    Diagram(), Spacer(1, 4),
    Table([["Máy", "Vai trò", "Cấu hình", "IP public"],
           ["cp (node1)", "control plane", "2 vCPU / 4GB, Ubuntu 24.04", "20.205.99.237"],
           ["worker1 (node2)", "worker", "2 vCPU / 4GB, Ubuntu 24.04", "23.100.92.133"],
           ["worker2 (node3)", "worker", "2 vCPU / 4GB, Ubuntu 24.04", "104.208.102.118"]],
          colWidths=[3.4 * cm, 3.2 * cm, 6 * cm, 3.6 * cm],
          style=TableStyle([("FONT", (0, 0), (-1, -1), "A", 9), ("FONT", (0, 0), (-1, 0), "AB", 9),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe9ff"))])),
    Spacer(1, 6),
    P("Phần mềm: Kubernetes v1.31, containerd, CNI flannel (dải Pod 10.244.0.0/16). Máy ảo thuộc Azure for "
      "Students, region East Asia."),
    P("2. Đóng gói ứng dụng bằng Docker", H1),
    P("Mỗi thành phần có một Dockerfile riêng: backend dùng <i>node:20-alpine</i>, frontend dùng "
      "<i>nginx:1.27-alpine</i>. Phiên bản được truyền qua tham số build <i>APP_VERSION</i> để phân biệt v1 "
      "và v2. Image gắn tag phiên bản, không dùng <i>latest</i>."),
    code("docker build -t dami1705/demo-backend:v1  --build-arg APP_VERSION=v1 app/backend\n"
         "docker build -t dami1705/demo-frontend:v1 --build-arg APP_VERSION=v1 app/frontend\n"
         "docker push dami1705/demo-backend:v1\n"
         "docker push dami1705/demo-frontend:v1\n"
         "# phiên bản mới\n"
         "docker build -t dami1705/demo-backend:v2 --build-arg APP_VERSION=v2 app/backend\n"
         "docker push dami1705/demo-backend:v2"),
    shot(1, "Trang Docker Hub hiển thị repo demo-backend, demo-frontend và các tag v1, v2", 3.8 * cm),
    PageBreak()]

story += [
    P("3. Dựng cluster Kubernetes", H1),
    P("Trên cả 3 máy: tắt swap, nạp module <i>overlay</i> và <i>br_netfilter</i>, bật <i>ip_forward</i>, cài "
      "containerd (SystemdCgroup=true), cài kubelet, kubeadm, kubectl v1.31 và <i>conntrack</i>. Đặt hostname "
      "lần lượt là cp, worker1, worker2."),
    code("# trên cp\n"
         "sudo kubeadm init --pod-network-cidr=10.244.0.0/16\n"
         "kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml\n"
         "# trên worker1, worker2\n"
         "sudo kubeadm join 172.16.0.4:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>"),
    shot(2, "kubectl get nodes -o wide: 3 node cp, worker1, worker2 đều Ready", 4 * cm),
    P("4. Triển khai ứng dụng lên Kubernetes", H1),
    P("Toàn bộ tài nguyên khai báo trong thư mục <i>k8s/</i> và tạo bằng <i>kubectl apply -f k8s/</i>: "
      "Namespace <b>demo-app</b>; hai Deployment (<b>backend</b>, <b>frontend</b>) mỗi cái 2 replicas, có "
      "readiness probe, giới hạn tài nguyên và <i>topologySpreadConstraints</i> theo "
      "<i>kubernetes.io/hostname</i> để dàn Pod lên cả 2 worker; Service <b>backend</b> (ClusterIP 3000) để "
      "frontend gọi backend qua DNS nội bộ; Service <b>frontend</b> (NodePort 30080) để truy cập từ trình duyệt."),
    code("kubectl apply -f k8s/\nkubectl get all -n demo-app -o wide"),
    shot(3, "kubectl get pods -n demo-app -o wide: Pod trải trên worker1 và worker2", 3.6 * cm),
    shot(4, "Trình duyệt truy cập http://23.100.92.133:30080, nút Gọi backend trả về JSON", 3.6 * cm),
    PageBreak()]

story += [
    P("5. Vận hành trên Kubernetes", H1),
    P("5.1 Scale", H2),
    P("Tăng Deployment backend từ 2 lên 4 replicas. Kubernetes chỉ thay đổi số replicas mong muốn rồi tự tạo "
      "thêm Pod và lập lịch lên các worker."),
    code("kubectl scale deploy/backend -n demo-app --replicas=4\n"
         "kubectl get pods -n demo-app -l app=backend -o wide"),
    shot(5, "Backend có 4 Pod Running trên các worker", 4.2 * cm),
    P("5.2 Cập nhật phiên bản mới và rollback", H2),
    P("Build image v2, push lên Docker Hub rồi đổi image của Deployment. Rolling update tạo Pod mới trước rồi "
      "mới xóa Pod cũ nên ứng dụng không gián đoạn. Sau đó dùng <i>rollout undo</i> để quay về v1."),
    code("kubectl set image deploy/backend backend=dami1705/demo-backend:v2 -n demo-app\n"
         "kubectl rollout status deploy/backend -n demo-app\n"
         "kubectl rollout history deploy/backend -n demo-app\n"
         "kubectl rollout undo deploy/backend -n demo-app"),
    shot(6, "API trả về version v2 sau khi cập nhật, và v1 sau khi rollback", 4.2 * cm),
    PageBreak()]

story += [
    P("5.3 Tắt một worker node: quan sát và giải thích", H2),
    P("Thao tác: dừng máy ảo worker2 trên Azure, theo dõi bằng <i>kubectl get nodes -w</i> và "
      "<i>kubectl get pods -n demo-app -o wide -w</i>, đồng thời truy cập ứng dụng qua IP của worker1."),
    P("<b>Diễn biến và giải thích:</b>"),
    P("1) Khi worker2 tắt, kubelet trên node đó ngừng gửi heartbeat. Sau khoảng 40 giây controller đánh dấu "
      "node là <b>NotReady</b> và gắn taint <i>node.kubernetes.io/unreachable</i>."),
    P("2) Ngay khi node NotReady, các Pod trên worker2 bị coi là không sẵn sàng nên Service loại chúng khỏi "
      "danh sách endpoint. Lưu lượng chỉ đi tới các Pod ở worker1, vì vậy người dùng vẫn truy cập được. Đây là "
      "lợi ích của việc chạy tối thiểu 2 replicas trên 2 worker khác nhau. Trong khoảng thời gian trước khi node "
      "bị đánh dấu NotReady, một số yêu cầu có thể lỗi do còn gửi tới Pod đã chết."),
    P("3) Sau khoảng 5 phút (tolerationSeconds mặc định 300 giây), Pod trên worker2 bị đưa ra khỏi node "
      "(Terminating/Unknown). ReplicaSet phát hiện thiếu Pod so với số replicas mong muốn nên tạo Pod thay thế, "
      "được lập lịch lên worker1."),
    P("4) Khi bật lại worker2, node trở về Ready nhưng các Pod <b>không tự chuyển ngược</b>, vì scheduler không "
      "cân bằng lại Pod đang chạy. Có thể dùng <i>kubectl rollout restart</i> để dàn lại."),
    shot(7, "kubectl get nodes -w: worker2 chuyển sang NotReady", 3.4 * cm),
    shot(8, "kubectl get pods -o wide -w: Pod được thay thế trên worker1", 3.4 * cm),
    shot(9, "Ứng dụng vẫn truy cập được qua worker1 khi worker2 đã tắt", 3.4 * cm),
    PageBreak()]

story += [P("6. Khó khăn gặp phải và cách xử lý", H1)]
for t in [
    "<b>Hạn mức Azure for Students:</b> chỉ cho phép một số region, tối đa 3 public IP và 6 core mỗi region nên "
    "không tạo thêm VM mới. Giải pháp: dùng lại 3 VM sẵn có (2 vCPU / 4GB), bật máy đang tắt, mở thêm cổng 30080 "
    "trên NSG.",
    "<b>Thiếu conntrack:</b> kubeadm init báo lỗi preflight <i>conntrack not found</i> trên Ubuntu 24.04. Khắc "
    "phục bằng cách cài gói conntrack (cùng socat, ebtables) trên cả 3 máy.",
    "<b>kubectl không chạy với user thường:</b> lỗi <i>connection to localhost:8080 refused</i> vì chưa có file "
    "~/.kube/config. Khắc phục bằng cách sao chép /etc/kubernetes/admin.conf vào ~/.kube/config.",
    "<b>Xung đột độ ưu tiên NSG:</b> rule mở cổng 30080 trùng priority với rule HTTP có sẵn. Đổi sang priority "
    "khác (350).",
    "<b>Pod dồn về một worker sau khi giảm replicas:</b> khi scale xuống, Kubernetes xóa Pod ở worker2 khiến cả "
    "hai Pod backend nằm ở worker1. Xóa một Pod để scheduler tạo lại ở worker2 nhờ topologySpreadConstraints.",
    "<b>Image phải public:</b> repository private trên Docker Hub khiến cluster không pull được image nếu chưa "
    "cấu hình imagePullSecret."]:
    story.append(P("• " + t))
story += [
    P("7. Kết luận", H1),
    P("Nhóm đã đóng gói ứng dụng bằng Docker, dựng cluster 1 control plane + 2 worker bằng kubeadm, triển khai "
      "bằng YAML và kubectl apply, thực hiện scale, cập nhật, rollback và kiểm thử sự cố tắt node. Mã nguồn, "
      "Dockerfile và file YAML nằm trong repository Git đính kèm.")]

SimpleDocTemplate("docs/Bao-cao.pdf", pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=2 * cm, title="Bao cao giua ky CKA 2026").build(story)
