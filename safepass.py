# وارد کردن کتابخانه‌های مورد نیاز
import customtkinter as ctk  # رابط گرافیکی مدرن‌تر بر پایه tkinter
from tkinter import messagebox  # برای نمایش پیام‌ها به کاربر
import random  # برای تولید رمز عبور تصادفی
import string  # برای استفاده از حروف و اعداد
import pyperclip  # برای کپی کردن متن به کلیپ‌بورد

# فهرست رمزهای رایج که امنیت کمی دارند
COMMON_PASSWORDS = {"123456", "password", "12345678", "qwerty", "123123", "admin"}

# کلاس تحلیل رمز عبور
class PasswordAnalyzer:
    def __init__(self, password):
        self.password = password  # ذخیره رمز عبور دریافتی

    # محاسبه امتیاز امنیتی رمز عبور
    def score(self):
        length = len(self.password)  # طول رمز
        has_digit = any(c.isdigit() for c in self.password)  # بررسی وجود رقم
        has_upper = any(c.isupper() for c in self.password)  # بررسی حروف بزرگ
        has_symbol = any(c in "!@#$%^&*()" for c in self.password)  # بررسی نمادها

        score = 0
        if length >= 8:
            score += 1
        if has_digit:
            score += 1
        if has_upper:
            score += 1
        if has_symbol:
            score += 1

        return score  # بازگرداندن امتیاز نهایی

    # بررسی اینکه آیا رمز عبور رایج است یا نه
    def is_common(self):
        return self.password.lower() in COMMON_PASSWORDS

    # تخمین زمان کرک رمز عبور
    def estimated_crack_time(self):
        complexity = 0
        if len(self.password) >= 8:
            complexity += 26
        if any(c.isupper() for c in self.password):
            complexity += 26
        if any(c.isdigit() for c in self.password):
            complexity += 10
        if any(c in "!@#$%^&*()" for c in self.password):
            complexity += 10

        if complexity == 0:
            return "کمتر از ۱ ثانیه"  # رمز بسیار ضعیف

        seconds = (complexity ** len(self.password)) / 1e6  # محاسبه زمان تقریبی بر حسب ثانیه
        units = [("ثانیه", 60), ("دقیقه", 60), ("ساعت", 24), ("روز", 365), ("سال", None)]
        for unit, limit in units:
            if not limit or seconds < limit:
                break
            seconds /= limit
        return f"{int(seconds)} {unit}"  # نمایش زمان با واحد مناسب

    # تولید رمز عبور پیشنهادی قوی
    def generate_strong_password(self, length=14):
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()", k=length))


# تنظیم حالت ظاهری برنامه
ctk.set_appearance_mode("Dark")  # حالت تاریک
ctk.set_default_color_theme("dark-blue")  # تم رنگی آبی تیره

# تعریف کلاس گرافیکی اصلی برنامه
class CyberGuard(ctk.CTk):
    def __init__(self):
        super().__init__()  # اجرای سازنده کلاس والد

        self.title("CyberGuard")  # عنوان پنجره
        self.geometry("700x700")  # اندازه پنجره
        self.resizable(False, False)  # جلوگیری از تغییر اندازه

        self.label = ctk.CTkLabel(self, text="ابزار تحلیل رمز عبور", font=("Vazirmatn", 22, "bold"))
        self.label.pack(pady=10)

        # فیلد ورود رمز عبور
        self.entry = ctk.CTkEntry(self, placeholder_text="رمز خود را وارد کنید", width=300, show="*")
        self.entry.pack(pady=5)

        # دکمه نمایش/مخفی کردن رمز
        self.show_password = False
        self.toggle_button = ctk.CTkButton(self, text="👁️", width=40, command=self.toggle_password_visibility)
        self.toggle_button.pack(pady=2)

        # لیبل نمایش نتیجه تحلیل
        self.result_label = ctk.CTkLabel(self, text="", text_color="lightgreen", font=("Vazirmatn", 16))
        self.result_label.pack(pady=5)

        # لیبل نمایش زمان کرک رمز
        self.crack_time_label = ctk.CTkLabel(self, text="", text_color="orange", font=("Vazirmatn", 14))
        self.crack_time_label.pack(pady=5)

        # لیبل نمایش رمز پیشنهادی
        self.suggested_label = ctk.CTkLabel(self, text="", text_color="skyblue", font=("Vazirmatn", 14))
        self.suggested_label.pack(pady=5)

        # نکات امنیتی برای کاربر
        self.tips = [
            "رمز عبور باید حداقل ۸ کاراکتر باشد.",
            "استفاده از اعداد و حروف بزرگ امنیت را افزایش می‌دهد.",
            "استفاده از نمادهایی مثل @ و # رمز را قوی‌تر می‌کند.",
            "رمز خود را هرچند وقت یک‌بار تغییر دهید.",
            "از رمزهای تکراری برای سایت‌های مختلف استفاده نکنید.",
        ]
        self.current_tip = 0
        self.tip_label = ctk.CTkLabel(self, text=self.tips[self.current_tip], text_color="gray", font=("Vazirmatn", 13))
        self.tip_label.pack(pady=5)
        self.next_tip_button = ctk.CTkButton(self, text="نکته بعدی", command=self.show_next_tip)
        self.next_tip_button.pack(pady=5)

        # دکمه‌های عملیاتی
        ctk.CTkButton(self, text="تحلیل رمز عبور", command=self.analyze_password).pack(pady=10)
        ctk.CTkButton(self, text="کپی رمز پیشنهادی", command=self.copy_suggested_password).pack(pady=5)
        ctk.CTkButton(self, text="درباره پروژه", command=self.show_about).pack(side="bottom", pady=10)

        self.suggested_password = ""  # متغیر ذخیره رمز پیشنهادی
        self.dark_mode = True  # حالت پیش‌فرض تم تاریک
        self.theme_button = ctk.CTkButton(self, text="روشن/تاریک", command=self.toggle_theme)
        self.theme_button.pack(pady=10)

    # تابع تغییر وضعیت نمایش رمز
    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.entry.configure(show="" if self.show_password else "*")
        self.toggle_button.configure(text="🙈" if self.show_password else "👁️")

    # تابع تغییر حالت روشن/تاریک
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        ctk.set_appearance_mode("Dark" if self.dark_mode else "Light")

    # نمایش نکته بعدی از لیست نکات
    def show_next_tip(self):
        self.current_tip = (self.current_tip + 1) % len(self.tips)
        self.tip_label.configure(text=self.tips[self.current_tip])

    # تحلیل رمز عبور وارد شده
    def analyze_password(self):
        pwd = self.entry.get()  # گرفتن رمز از ورودی
        if not pwd:
            self.result_label.configure(text="لطفاً رمز عبور را وارد کنید.")
            return

        analyzer = PasswordAnalyzer(pwd)

        if analyzer.is_common():  # اگر رمز رایج باشد
            self.result_label.configure(text="این رمز عبور بسیار رایج است!")
        else:
            score = analyzer.score()  # محاسبه امتیاز امنیت
            msg = ["رمز بسیار ضعیف است.",
                   "رمز نسبتاً ضعیف است.",
                   "رمز متوسط است.",
                   "رمز قوی است.",
                   "رمز بسیار قوی است."][score]
            self.result_label.configure(text=msg)

        self.crack_time_label.configure(text=f"زمان تقریبی کرک: {analyzer.estimated_crack_time()}")  # نمایش زمان کرک
        self.suggested_password = analyzer.generate_strong_password()  # تولید رمز پیشنهادی
        self.suggested_label.configure(text=f"رمز پیشنهادی: {self.suggested_password}")  # نمایش رمز پیشنهادی

    # کپی رمز پیشنهادی در کلیپ‌بورد
    def copy_suggested_password(self):
        if self.suggested_password:
            pyperclip.copy(self.suggested_password)
            messagebox.showinfo("کپی شد", "رمز پیشنهادی در کلیپ‌بورد کپی شد.")

    # نمایش اطلاعات درباره پروژه
    def show_about(self):
        messagebox.showinfo("درباره پروژه",
            "این پروژه برای افزایش امنیت رمزهای عبور طراحی شده است.\n"
            "توسعه‌دهندگان: امیرپارسا و ایلیا\n"
            "استفاده از Python و کتابخانه CustomTkinter\n"
            "نسخه ارتقاءیافته با تحلیل پیشرفته رمز"
        )

# اجرای برنامه
if __name__ == "__main__":
    app = CyberGuard()  # ایجاد شیء از کلاس CyberGuard
    app.mainloop()  # اجرای حلقه اصلی برنامه گرافیکی