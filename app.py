import streamlit as st
import nbformat
from nbconvert import PythonExporter
import io
import zipfile
import time

# إعداد واجهة الصفحة
st.set_page_config(page_title="Jupyter to Python Converter", page_icon="🐍")

# اختيار اللغة
lang = st.sidebar.selectbox(
    "🌐 اختر اللغة | Select Language | 选择语言", 
    ["العربية","English", "中文"]
)

# تحديد اتجاه الصفحة بناءً على اللغة المختارة
if lang == "العربية":
    st.markdown(
        """
        <style>
            body { direction: rtl; text-align: right; }
            .stButton button { float: left; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            body { direction: ltr; text-align: left; }
        </style>
        """,
        unsafe_allow_html=True
    )

# النصوص حسب اللغة
texts = {
    "title": {
        "English": "🔄 Jupyter to Python Converter",
        "العربية": "🔄 محول Jupyter إلى Python",
        "中文": "🔄 Jupyter 转 Python 转换器"
    },
    "caption": {
        "English": "Upload `.ipynb` files and convert them to Python scripts.",
        "العربية": "ارفع ملفات `.ipynb` وسيتم تحويلها إلى سكربتات Python.",
        "中文": "上传 `.ipynb` 文件，转换为 Python 脚本。"
    },
    "remove_md": {
        "English": "📝 Remove Markdown cells",
        "العربية": "📝 حذف خلايا Markdown",
        "中文": "📝 删除 Markdown 单元"
    },
    "upload": {
        "English": "Upload one or multiple files",
        "العربية": "ارفع ملف أو عدة ملفات",
        "中文": "上传一个或多个文件"
    },
    "reset": {
        "English": "🔄 Reset Page",
        "العربية": "🔄 إعادة تعيين الصفحة",
        "中文": "🔄 重置页面"
    },
    "converted": {
        "English": "📄 Converted Files:",
        "العربية": "📄 الملفات المحوّلة:",
        "中文": "📄 已转换的文件："
    },
    "code_cells": {
        "English": "📊 Number of code cells after cleaning:",
        "العربية": "📊 عدد خلايا الكود بعد الحذف:",
        "中文": "📊 清理后代码单元数量："
    },
    "download_file": {
    "English": "Download File",
    "العربية": "تحميل الملف",
    "中文": "下载文件"
    },
    "download_all": {
        "English": "📦 Download all as ZIP",
        "العربية": "📦 تحميل جميع الملفات كـ ZIP",
        "中文": "📦 全部下载为 ZIP"
    },
    "converted_success": {
        "English": "✅ Converted:",
        "العربية": "✅ تم تحويل:",
        "中文": "✅ 已转换："
    },
    "error": {
        "English": "❌ Error in file:",
        "العربية": "❌ خطأ في الملف:",
        "中文": "❌ 文件错误："
    }
}

# الواجهة
st.title(texts["title"][lang])
st.caption(texts["caption"][lang])

remove_markdown = st.checkbox(texts["remove_md"][lang])

uploaded_files = st.file_uploader(
    texts["upload"][lang],
    type=["ipynb"],
    accept_multiple_files=True
)

if st.button(texts["reset"][lang]):
    st.rerun()
converted_files = []

if uploaded_files:
    total_files = len(uploaded_files)
    progress = st.progress(0)

    st.write("---")
    st.subheader(texts["converted"][lang])

    for i, file in enumerate(uploaded_files):
        try:
            notebook = nbformat.read(file, as_version=4)

            if remove_markdown:
                notebook['cells'] = [cell for cell in notebook['cells'] if cell['cell_type'] != 'markdown']

            exporter = PythonExporter()
            script, _ = exporter.from_notebook_node(notebook)
            py_filename = file.name.replace(".ipynb", ".py")

            converted_files.append((py_filename, script))

            # ✅ رسالة التحويل مع زر التحميل بجانبها
            col1, col2 = st.columns([5, 1])
            with col1:
                st.success(f"{texts['converted_success'][lang]} {file.name}")
            with col2:
                st.download_button(
                    label=f"⬇️ {texts['download_file'][lang]}",
                    data=script,
                    file_name=py_filename,
                    mime="text/x-python",
                    key=py_filename
                

    )


            # ✅ عدد خلايا الكود يظهر فقط إذا حذف Markdown مفعّل
            if remove_markdown:
                code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
                st.info(f"{texts['code_cells'][lang]} {len(code_cells)}")

        except Exception as e:
            st.error(f"{texts['error'][lang]} {file.name} : {e}")

        progress.progress((i + 1) / total_files)
        time.sleep(0.2)

    st.write("---")

    if len(converted_files) > 1:
        output_zip = io.BytesIO()
        with zipfile.ZipFile(output_zip, "w") as zf:
            for py_filename, script in converted_files:
                zf.writestr(py_filename, script)
        output_zip.seek(0)

        st.download_button(
            label=texts["download_all"][lang],
            data=output_zip,
            file_name="converted_scripts.zip",
            mime="application/zip"
        )

