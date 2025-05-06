import customtkinter as ctk
from tkinter import messagebox
import random, string, pyperclip

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class CyberGuard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CyberGuard")
        self.geometry("700x500")

        self.entry = ctk.CTkEntry(self, placeholder_text="رمز خود را وارد کنید", width=300)
        self.label = ctk.CTkLabel(self, text="ابزار تحلیل رمز عبور", font=("Vazirmatn", 22, "bold"))
        self.result_label = ctk.CTkLabel(self, text="", text_color="lightgreen", font=("Vazirmatn", 16))
        self.crack_time_label = ctk.CTkLabel(self, text="", text_color="orange", font=("Vazirmatn", 14))
        self.suggested_label = ctk.CTkLabel(self, text="", text_color="skyblue", font=("Vazirmatn", 14))
        
        ctk.CTkButton(self, text="رمز تحلیل", command=self.analyze_password).pack(pady=10)
        ctk.CTkButton(self, text="پیشنهادی رمز کپی", command=self.copy_suggested_password).pack(pady=5)
        ctk.CTkButton(self, text="پروژه درباره", command=self.show_about).pack(side="bottom", pady=10)

        for widget in [self.label, self.entry, self.result_label, self.crack_time_label, self.suggested_label]:
            widget.pack(pady=10)

        self.suggested_password = ""

    def analyze_password(self):
        pwd = self.entry.get()
        score = sum([len(pwd) >= 8, any(c.isdigit() for c in pwd),
                     any(c.isupper() for c in pwd), any(c in "!@#$%^&*()" for c in pwd)])
        complexity = sum([26 if len(pwd) >= 8 else 0,
                          10 if any(c.isdigit() for c in pwd) else 0,
                          26 if any(c.isupper() for c in pwd) else 0,
                          10 if any(c in "!@#$%^&*()" for c in pwd) else 0])

        msg = ["رمز عبور ضعیف است. حتما آن را تغییر دهید.",
               "رمز متوسط است. بهتر است پیچیده‌تر شود.",
               "رمز عبور قوی است."][score > 1 + (score == 4)]
        self.result_label.configure(text=msg)
        
        
#برسی زمان کرک شدن رمز 


        seconds = (complexity ** len(pwd)) / 1e9
        units = [("ثانیه", 60), ("دقیقه", 60), ("ساعت", 24), ("روز", 365), ("سال", None)]
        for unit, limit in units:
            if not limit or seconds < limit:
                break
            seconds /= limit
        self.crack_time_label.configure(text=f"زمان تقریبی برای کرک شدن: {int(seconds)} {unit}")

        self.suggested_password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()", k=14))
        self.suggested_label.configure(text=f"رمز پیشنهادی: {self.suggested_password}")

    def copy_suggested_password(self):
        if self.suggested_password:
            pyperclip.copy(self.suggested_password)
            messagebox.showinfo("کپی شد", "رمز پیشنهادی در کلیپ‌بورد کپی شد.")


#درباره پروژه و کدنویسی و توضیح


    def show_about(self):
        messagebox.showinfo("درباره پروژه",
            "با سلام خدمت داوران محترم استان لرستان.\n"
            "این پروژه با هدف افزایش امنیت رمزهای عبور طراحی شده است تا کاربران در برابر حملات بروت‌فورس محفوظ بمانند.\n"
            "برنامه با زبان پایتون و کتابخانه CustomTkinter توسعه یافته و طراحی و کدنویسی توسط امیرپارسا و ایلیا انجام شده است."
        )


if __name__ == "__main__":
    app = CyberGuard()
    app.mainloop()