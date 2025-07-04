import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import nbformat
from nbconvert import PythonExporter
import os

# 🗂️ القاموس متعدد اللغات
texts = {
    "title": {
        "العربية": "🔄 محول ipynb إلى Py",
        "English": "🔄 ipynb to Py Converter",
        "中文": "🔄 ipynb 转 Py 转换器"
    },
    "select_file": {
        "العربية": "📂 اختر ملف جوبيتر أو اسحبه هنا",
        "English": "📂 Select or drag ipynb file here",
        "中文": "📂 选择或拖放 ipynb 文件"
    },
    "select_file2": {
        "العربية": "📂 ipynb اختر ملف ",
        "English": "📂 Select ipynb file ",
        "中文": "📂 选择 ipynb 文件"
    },    
    "remove_md": {
        "العربية": "📝 حذف Markdown",
        "English": "📝 Remove Markdown",
        "中文": "📝 删除 Markdown"
    },
    "convert": {
        "العربية": "🚀 تحويل",
        "English": "🚀 Convert",
        "中文": "🚀 转换"
    },
    "success": {
        "العربية": "✅ تم التحويل إلى:",
        "English": "✅ Converted to:",
        "中文": "✅ 已转换为:"
    },
    "error": {
        "العربية": "❌ خطأ في التحويل:",
        "English": "❌ Conversion Error:",
        "中文": "❌ 转换错误:"
    },
    "warning": {
        "العربية": "⚠️ اختر ملفات بامتداد .ipynb فقط",
        "English": "⚠️ Please select .ipynb files only",
        "中文": "⚠️ 请选择 .ipynb 文件"
    },
    "about_text": {
        "العربية": "🛠️ الأداة من تطوير أحمد الفكي | Black.Ice.Onet@gmail.com | جميع الحقوق محفوظة | يدعم سحب الملف للمربع",
        "English": "🛠️ Tool developed by Ahmed Elfaki | Black.Ice.Onet@gmail.com | All Rights Reserved | Drag & Drop supported",
        "中文": "🛠️ 工具由 Ahmed Elfaki 开发 | Black.Ice.Onet@gmail.com | 版权所有 | 支持拖放文件"
    }
}

# 🌐 نافذة اختيار اللغة
def choose_language():
    lang_win = tk.Tk()
    lang_win.title("🌐 اختر اللغة | Select Language | 选择语言")
    lang_win.geometry("300x150")
    lang_var = tk.StringVar(value="العربية")

    tk.Label(lang_win, text="🌐 اختر اللغة | Select Language | 选择语言", pady=10).pack()
    langs = ["العربية", "English", "中文"]
    for l in langs:
        tk.Radiobutton(lang_win, text=l, variable=lang_var, value=l).pack(anchor="w")

    def confirm():
        lang_win.destroy()

    tk.Button(lang_win, text="✔️ OK", command=confirm).pack(pady=10)
    lang_win.mainloop()
    return lang_var.get()

# 🔥 تشغيل اختيار اللغة
lang = choose_language()

# 🖥️ الواجهة الرئيسية
root = TkinterDnD.Tk()
root.title(texts["title"][lang])
root.geometry("500x300")

selected_files = []

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text=texts["select_file"][lang])
label.pack()

entry = tk.Entry(frame, width=50)
entry.pack(pady=5)

remove_md_var = tk.BooleanVar()
remove_md_cb = tk.Checkbutton(frame, text=texts["remove_md"][lang], variable=remove_md_var)
remove_md_cb.pack()

# 🎯 دالة السحب والإفلات
def drop(event):
    files = root.tk.splitlist(event.data)
    for file in files:
        if file.endswith(".ipynb"):
            selected_files.append(file)
        else:
            messagebox.showwarning("⚠️", texts["warning"][lang])
    update_entry()

# 📂 دالة اختيار الملفات يدويًا
def browse():
    files = filedialog.askopenfilenames(filetypes=[("Jupyter Notebooks", "*.ipynb")])
    for file in files:
        selected_files.append(file)
    update_entry()

# 🔧 تحديث الحقل
def update_entry():
    entry.delete(0, tk.END)
    entry.insert(0, "; ".join(selected_files))

# 🚀 دالة التحويل
def convert():
    if not selected_files:
        messagebox.showwarning("⚠️", texts["warning"][lang])
        return

    for file in selected_files:
        try:
            notebook = nbformat.read(file, as_version=4)
            if remove_md_var.get():
                notebook['cells'] = [cell for cell in notebook['cells'] if cell['cell_type'] != 'markdown']
            exporter = PythonExporter()
            script, _ = exporter.from_notebook_node(notebook)
            output_file = file.replace(".ipynb", ".py")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(script)
            messagebox.showinfo("✅", f"{texts['success'][lang]} {output_file}")
        except Exception as e:
            messagebox.showerror("❌", f"{texts['error'][lang]} {e}")

# 🔘 أزرار
btn_browse = tk.Button(frame, text=texts["select_file2"][lang], command=browse)
btn_browse.pack(pady=5)

btn_convert = tk.Button(frame, text=texts["convert"][lang], command=convert)
btn_convert.pack(pady=5)

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)

# ✅ ملاحظة وحقوق
tk.Label(root, text=texts["about_text"][lang], fg="gray", font=("Arial", 8), wraplength=480, justify="center").pack(side="bottom", pady=5)

root.mainloop()

