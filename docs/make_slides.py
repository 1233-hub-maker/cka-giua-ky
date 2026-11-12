"""Tạo docs/Thuyet-trinh.pptx. Ảnh lấy từ docs/images/<n>.png nếu có, nếu không để khung trống."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

NAVY = RGBColor(0x1A, 0x3C, 0x6E)
GREY = RGBColor(0x55, 0x55, 0x55)
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, s, size=18, bold=False, color=RGBColor(0x22, 0x22, 0x22), align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = s if isinstance(s, list) else [s]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(6)
        r = p.add_run()
        r.text = line
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, "Arial"
        r.font.color.rgb = color
    return tb


def box(slide, x, y, w, h, label, fill="#dbe9ff", size=13, bold=True):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor.from_string(fill.lstrip("#").upper())
    sh.line.color.rgb = NAVY
    tf = sh.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size, r.font.bold, r.font.name = Pt(size), bold, "Arial"
    r.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    return sh


def arrow(slide, x1, y1, x2, y2):
    c = slide.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = GREY
    c.line.width = Pt(1.5)


def slide(title):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.0))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    text(s, 0.5, 0.18, 12.3, 0.7, title, 28, True, RGBColor(255, 255, 255))
    return s


def pic(s, n, caption, x, y, w, h):
    """Chèn ảnh số n vừa khung (x,y,w,h); thiếu ảnh thì vẽ khung trống."""
    for ext in ("png", "jpg", "jpeg"):
        path = os.path.join("docs", "images", "%s.%s" % (n, ext))
        if os.path.exists(path):
            from PIL import Image
            iw, ih = Image.open(path).size
            k = min(w / iw, h / ih)
            pw, ph = iw * k, ih * k
            s.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y), Inches(pw), Inches(ph))
            text(s, x, y + ph + 0.02, w, 0.35, caption, 11, False, GREY, PP_ALIGN.CENTER)
            return
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.background()
    sh.line.color.rgb = RGBColor(0x99, 0x99, 0x99)
    sh.line.dash_style = 4
    tf = sh.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "[ Ảnh: %s ]" % caption
    r.font.size, r.font.name = Pt(13), "Arial"
    r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)


def bullets(s, items, x=0.6, y=1.35, w=5.6, size=18):
    text(s, x, y, w, 5.5, ["•  " + i for i in items], size)


# 1. Tiêu đề
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
text(s, 0.8, 2.2, 11.7, 1.4, "Triển khai ứng dụng web với Docker và Kubernetes", 40, True, RGBColor(255, 255, 255))
text(s, 0.8, 3.9, 11.7, 0.8, "Bài tập giữa kỳ – Khoá CKA 2026", 24, False, RGBColor(0xDB, 0xE9, 0xFF))
text(s, 0.8, 5.2, 11.7, 1.0, ["Nhóm: ……………………   |   Thành viên (5): ……………………………", "Ngày nộp: 19/11/2026"],
     18, False, RGBColor(0xDB, 0xE9, 0xFF))

# 2. Mục tiêu và kiến trúc
s = slide("Mục tiêu và kiến trúc")
bullets(s, ["Đóng gói ứng dụng frontend + backend bằng Docker",
            "Dựng cluster Kubernetes: 1 control plane + 2 worker (kubeadm)",
            "Triển khai bằng YAML, vận hành: scale, update, rollback",
            "Thử nghiệm sự cố: tắt một worker"], w=5.4, size=17)
box(s, 8.0, 1.3, 2.6, 0.6, "Trình duyệt  :30080", "#fff3cd")
box(s, 7.6, 2.3, 3.4, 0.6, "Service frontend (NodePort)", "#e2f0d9", 12)
arrow(s, 9.3, 1.9, 9.3, 2.3)
box(s, 6.3, 3.4, 2.0, 3.4, "cp\ncontrol plane\nflannel", "#f4f4f4", 12)
box(s, 8.5, 3.4, 2.2, 3.4, "worker1", "#f4f4f4", 12)
box(s, 10.9, 3.4, 2.2, 3.4, "worker2", "#f4f4f4", 12)
for x in (8.65, 11.05):
    box(s, x, 4.3, 1.9, 0.65, "Pod frontend", "#c6e0b4", 11)
    box(s, x, 5.4, 1.9, 0.65, "Pod backend", "#f8cbad", 11)
    arrow(s, 9.3, 2.9, x + 0.95, 4.3)

# 3. Docker
s = slide("1. Đóng gói bằng Docker")
bullets(s, ["Mỗi thành phần một Dockerfile: backend (node:20-alpine), frontend (nginx:1.27-alpine)",
            "Phiên bản qua build-arg APP_VERSION",
            "Đẩy lên Docker Hub: dami1705/demo-backend (v1, v2), demo-frontend (v1)",
            "Gắn tag phiên bản, không dùng latest"], w=5.7, size=17)
pic(s, 1, "Docker Hub: các repo và tag", 6.6, 1.4, 6.3, 5.0)

# 4. Cluster
s = slide("2. Dựng cluster Kubernetes")
bullets(s, ["3 VM Azure (2 vCPU / 4GB, Ubuntu 24.04): cp, worker1, worker2",
            "Cài containerd, kubeadm, kubelet, kubectl v1.31",
            "kubeadm init trên cp, kubeadm join trên 2 worker",
            "CNI: flannel (10.244.0.0/16)",
            "kubectl get nodes: 3 node Ready"], w=5.7, size=17)
pic(s, 2, "kubectl get nodes -o wide", 6.6, 1.4, 6.3, 4.5)

# 5. Triển khai
s = slide("3. Triển khai ứng dụng")
bullets(s, ["Namespace riêng: demo-app",
            "Deployment backend và frontend, mỗi cái 2 replicas",
            "topologySpreadConstraints: Pod dàn đều 2 worker",
            "Service backend (ClusterIP) cho frontend gọi backend; Service frontend (NodePort 30080)",
            "Toàn bộ khai báo bằng YAML: kubectl apply -f k8s/"], w=5.7, size=17)
pic(s, 3, "kubectl get pods -o wide", 6.6, 1.4, 6.3, 4.5)

# 6. Truy cập
s = slide("4. Truy cập ứng dụng từ trình duyệt")
bullets(s, ["Mở http://<IP worker>:30080",
            "Nút \"Gọi backend\" trả về phiên bản, tên Pod, số lượt gọi",
            "Tên Pod đổi giữa các lần bấm: Service chia tải",
            "NodePort mở trên mọi node"], w=5.4, size=17)
pic(s, 4, "Giao diện ứng dụng", 6.2, 1.4, 6.7, 5.0)

# 7. Scale
s = slide("5. Scale lên 4 replicas")
text(s, 0.6, 1.35, 12, 0.8, "kubectl scale deploy/backend -n demo-app --replicas=4", 20, True, NAVY)
bullets(s, ["Chỉ đổi số replicas mong muốn", "Kubernetes tự tạo thêm Pod và lập lịch lên worker",
            "Số Pod luôn bám theo con số đã đặt"], y=2.3, w=5.4, size=17)
pic(s, 5, "4 Pod backend Running", 6.2, 2.2, 6.7, 4.3)

# 8. Update / rollback
s = slide("6. Cập nhật phiên bản và rollback")
text(s, 0.6, 1.3, 12, 1.2, ["kubectl set image deploy/backend backend=dami1705/demo-backend:v2",
                            "kubectl rollout undo deploy/backend -n demo-app"], 17, True, NAVY)
bullets(s, ["Rolling update: Pod mới tạo trước, Pod cũ xóa dần, không gián đoạn",
            "Kubernetes lưu lịch sử nên rollback nhanh",
            "Trình duyệt: v1 → v2 → v1"], y=2.6, w=5.4, size=17)
pic(s, 6, "Phiên bản v2 và sau rollback v1", 6.2, 2.6, 6.7, 3.9)

# 9. Tắt worker
s = slide("7. Tắt một worker node")
bullets(s, ["~40 giây: node chuyển NotReady",
            "Service loại Pod của node đó: ứng dụng vẫn chạy nhờ Pod ở worker còn lại",
            "~5 phút: Pod bị xóa, ReplicaSet tạo Pod thay thế trên worker còn lại",
            "Bật lại node: Pod không tự chuyển ngược"], w=5.6, size=16)
pic(s, 7, "worker2 NotReady", 6.4, 1.3, 6.5, 1.7)
pic(s, 8, "Pod được thay thế", 6.4, 3.4, 6.5, 1.7)
pic(s, 9, "App vẫn truy cập được", 6.4, 5.5, 6.5, 1.6)

# 10. Khó khăn
s = slide("8. Khó khăn và cách xử lý")
bullets(s, ["Hạn mức Azure for Students (3 IP, 6 core): dùng lại VM sẵn có, mở cổng 30080 trên NSG",
            "kubeadm báo thiếu conntrack trên Ubuntu 24.04: cài gói conntrack",
            "kubectl không chạy với user thường: sao chép admin.conf vào ~/.kube/config",
            "Pod dồn về một worker sau khi giảm replicas: xóa Pod để scheduler dàn lại",
            "Image phải public để cluster pull được"], w=12, size=19)

# 11. Kết luận
s = slide("Kết luận")
bullets(s, ["Hoàn thành đóng gói, dựng cluster, triển khai, scale, update, rollback",
            "Kiểm chứng khả năng chịu lỗi khi mất một worker",
            "Mã nguồn, Dockerfile, YAML và hướng dẫn nằm trong repository Git",
            "Cảm ơn thầy cô và các bạn đã lắng nghe"], w=12, size=22)

prs.save("docs/Thuyet-trinh.pptx")
print("slides:", len(prs.slides))
