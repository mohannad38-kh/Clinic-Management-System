from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk  # pip install pillow
import time

from xrays import XraysClass
from dental import DentalClass
from implant import ImplantClass
from fillings import FillingsClass  

class Clinic:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x650+50+20")
        self.root.resizable(False, False)
        self.root.title("Clinic Management System")
        self.root.config(bg="#EDF2F7") # خلفية عامة رمادية فاتحة ناعمة

        self.base_dir = Path(__file__).resolve().parent
 
        #========================== الشريط العلوي العصري (Modern Header) ========================== 
        header_frame = Frame(self.root, bg='#0f172a', bd=0) # لون كحلي داكن عصري جداً
        header_frame.place(x=0, y=0, width=1200, height=60)

        lbl_system_title = Label(
            header_frame, 
            text="🏥 نظام إدارة عيادة الأسنان ", 
            font=("Segoe UI", 14, 'bold'), 
            bg='#0f172a', 
            fg='#38bdf8'
        )
        lbl_system_title.pack(side=LEFT, padx=20)

        self.lbl_date = Label(
            header_frame, 
            text="Date: DD-MM-YYYY   |   Time: HH:MM:SS", 
            font=("Segoe UI", 11), 
            bg='#0f172a', 
            fg='#cbd5e1'
        )
        self.lbl_date.pack(side=RIGHT, padx=20)
        self.timed()
        
        #========================== القائمة الجانبية (Sidebar) ==========================
        sidebar_frame = Frame(self.root, bg='#ffffff', bd=0)
        sidebar_frame.place(x=985, y=60, width=215, height=590)
        
        #========================== صورة الشعار في القائمة ==========================
        try:
            self.menu_img = Image.open(self.base_dir / "images" / "log.jpg")
            self.menu_img = self.menu_img.resize((215, 130), Image.Resampling.LANCZOS)
            self.menu_img = ImageTk.PhotoImage(self.menu_img)
            
            lbl_menu_img = Label(sidebar_frame, image=self.menu_img, bg='white', bd=0)
            lbl_menu_img.pack(side=TOP, fill=X)
        except Exception:
            pass
        
        # عنوان صغير للقائمة
        lbl_nav = Label(sidebar_frame, text="لوحة التحكم", font=('Segoe UI', 11, 'bold'), bg="#ffffff", fg='#64748b')
        lbl_nav.pack(side=TOP, anchor='w', padx=15, pady=(10, 5))
        
        #========================= دالة لتصميم الأزرار بشكل احترافي مع تفاعل الماوس ========================
        def create_modern_button(parent, text, command, bg_color="#f8fafc", fg_color="#334155", hover_bg="#0284c7", hover_fg="#ffffff"):
            btn = Button(
                parent, text=text, command=command,
                font=('Segoe UI', 11, 'bold'),
                bg=bg_color, fg=fg_color,
                activebackground=hover_bg, activeforeground=hover_fg,
                bd=0, cursor='hand2', anchor='w', padx=15, pady=8
            )
            
            # إضافة تأثير مرور الماوس (Hover Effect)
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg, fg=hover_fg))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_color, fg=fg_color))
            return btn

        # الأزرار مع الرموز المعبرة
        btn1 = create_modern_button(sidebar_frame, '   📅  الحجوزات', self.dental)
        btn1.pack(side=TOP, fill=X, padx=10, pady=3)
        
        btn2 = create_modern_button(sidebar_frame, '   🔬  الأشعة', self.xrays)
        btn2.pack(side=TOP, fill=X, padx=10, pady=3)
        
        btn3 = create_modern_button(sidebar_frame, '   🦷  زراعة الأسنان', self.implant)
        btn3.pack(side=TOP, fill=X, padx=10, pady=3)
        
        # تم تغيير رمز قسم الحشوات إلى رمز الإبرة/الحقنة العلاجية 💉 (أو يمكنك استبداله بـ 🩹 أو ✨ حسب رغبتك)
        btn4 = create_modern_button(sidebar_frame, '   💉  قسم الحشوات', self.fillings)
        btn4.pack(side=TOP, fill=X, padx=10, pady=3)
        
        # زر الخروج برمز عصري
        btn_exit = create_modern_button(
            sidebar_frame, '   ⏻  إغلاق النظام', self.root.destroy,
            bg_color="#fef2f2", fg_color="#dc2626", hover_bg="#dc2626", hover_fg="#ffffff"
        )
        btn_exit.pack(side=BOTTOM, fill=X, padx=10, pady=15)
        
        #========================= إطار الصورة الرئيسية (Main Display Area) =================
        content_frame = Frame(self.root, bg='#ffffff', bd=0)
        content_frame.place(x=0, y=60, width=985, height=590)
        
        try:
            self.logo = Image.open(self.base_dir / "images" / "logo.jpg")
            self.log = ImageTk.PhotoImage(self.logo.resize((985, 590), Image.Resampling.LANCZOS))
            
            lbl_logo_image = Label(content_frame, image=self.log, bg='white', bd=0)
            lbl_logo_image.place(x=0, y=0, width=985, height=590)
        except Exception:
            pass
        
    #========================= تحديث التاريخ والوقت بداخل الشريط العلوي ========================
    def timed(self):
        time_ = time.strftime("%I:%M:%S %p")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_date.config(
            text=f"Date: {date_}   |   Time: {time_}"
        )
        self.root.after(1000, self.timed)
    
    def xrays(self):
        self.new_window = Toplevel(self.root)
        self.new_opj = XraysClass(self.new_window)
        
    def dental(self):
        self.new_win = Toplevel(self.root)
        self.new_opj = DentalClass(self.new_win)
  
    def implant(self):
        self.new_win = Toplevel(self.root)
        self.new_opj = ImplantClass(self.new_win)
    
    def fillings(self):
        self.new_win = Toplevel(self.root)
        self.new_opj = FillingsClass(self.new_win)

if __name__ == "__main__":
    root = Tk()
    obj = Clinic(root)
    root.mainloop()