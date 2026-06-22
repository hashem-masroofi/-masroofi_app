import flet as ft
from datetime import datetime
import sqlite3

APP_VERSION = "1.0"
DB_PATH = "masroofi.db"
BG_IMAGE = "background.png"

days_ar = {"Saturday":"السبت","Sunday":"الأحد","Monday":"الاثنين","Tuesday":"الثلاثاء","Wednesday":"الأربعاء","Thursday":"الخميس","Friday":"الجمعة"}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            note TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def main(page: ft.Page):
    page.title = f"مصروفي v{APP_VERSION}"
    page.rtl = True
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.window_resizable = True
    
    init_db()
    conn = sqlite3.connect(DB_PATH)
    
        # --- بداية كود الخلفية ---
    page.assets_dir = "assets"
    page.bgcolor = ft.Colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="background.png",
            fit=ft.ImageFit.COVER,
            opacity=0.85
        )
    )
    # --- نهاية كود الخلفية ---
    
    
 
    
    name = ft.TextField(label="اسم المصروف", border_color="#FFD700", color="white", label_style=ft.TextStyle(color="white70"), cursor_color="#FFD700", bgcolor="#00000080")
    amount = ft.TextField(label="المبلغ", border_color="#FFD700", color="white", label_style=ft.TextStyle(color="white70"), cursor_color="#FFD700", keyboard_type=ft.KeyboardType.NUMBER, bgcolor="#00000080")
    category = ft.Dropdown(label="التصنيف", border_color="#FFD700", color="white", label_style=ft.TextStyle(color="white70"), bgcolor="#00000080", options=[ft.dropdown.Option("أكل"), ft.dropdown.Option("مواصلات"), ft.dropdown.Option("فواتير"), ft.dropdown.Option("ترفيه"), ft.dropdown.Option("أخرى")], value="أكل")
    
    expenses_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    
    def delete_expense(expense_id, expense_container):
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
        expenses_list.controls.remove(expense_container)
        page.snack_bar = ft.SnackBar(ft.Text("تم حذف المصروف"), bgcolor="green")
        page.snack_bar.open = True
        page.update()
    
    def create_expense_card(expense_id, note, amt, cat, created_at):
        dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        day_ar = days_ar[dt.strftime("%A")]
        date_time_str = f"{day_ar} {dt.strftime('%Y/%m/%d')} الساعة {dt.strftime('%I:%M %p')}"
        
        expense_container = ft.Container()
        expense_container.content=ft.Column([
            ft.Row([
                ft.Text(f"{note}", expand=True, color="white", weight="bold", size=16),
                ft.Text(f"{amt} ريال", color="#FFD700", weight="bold", size=16),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color="red400",
                    tooltip="حذف",
                    on_click=lambda e: delete_expense(expense_id, expense_container)
                )
            ]),
            ft.Row([
                ft.Container(
                    content=ft.Text(cat, size=11, color="black"),
                    bgcolor="#FFD700",
                    padding=ft.padding.symmetric(4, 8),
                    border_radius=12
                ),
                ft.Text(date_time_str, size=11, color="white")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=5)
        
        expense_container.bgcolor="#000000B3"
        expense_container.padding=15
        expense_container.border_radius=15
        expense_container.border=ft.border.all(1, "#FFFFFF4D")
        return expense_container
    
    def add_expense(e):
        if name.value and amount.value:
            try:
                cur = conn.cursor()
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("INSERT INTO expenses(amount, category, note, created_at) VALUES(?,?,?,?)", (float(amount.value), category.value, name.value, current_time))
                conn.commit()
                expense_id = cur.lastrowid
                expenses_list.controls.insert(0, create_expense_card(expense_id, name.value, float(amount.value), category.value, current_time))
                name.value = ""
                amount.value = ""
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"خطأ: {ex}"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
    
    def load_expenses():
        cur = conn.cursor()
        cur.execute("SELECT id, note, amount, category, created_at FROM expenses ORDER BY id DESC")
        for expense_id, note, amt, cat, created_at in cur.fetchall():
            expenses_list.controls.append(create_expense_card(expense_id, note, amt, cat, created_at))
        page.update()
    
    load_expenses()
    
    page.add(
        ft.Stack([
            
            
            # الضباب البنفسجي من فوق
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=["#8B5CF6CC", "#8B5CF600"],  # بنفسجي غامق -> شفاف
                    stops=[0.0, 1.0]
                ),
                height=200,
                expand=True,
                top=0,
            ),
            
            # الضباب البنفسجي من تحت
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.bottom_center,
                    end=ft.alignment.top_center,
                    colors=["#8B5CF6CC", "#8B5CF600"],  # بنفسجي غامق -> شفاف
                    stops=[0.0, 1.0]
                ),
                height=250,
                expand=True,
                bottom=0,
            ),
            
            # المحتوى حقك
            ft.Container(
                content=ft.Column([
                    ft.Container(content=ft.Column([ft.Row([ft.Text(f"v{APP_VERSION}", size=12, color="white")], alignment=ft.MainAxisAlignment.END), ft.Text("مصروفي", size=32, color="white", weight="bold"), ft.Text(f"اليوم: {days_ar[datetime.now().strftime('%A')]} - {datetime.now().strftime('%Y/%m/%d')}", size=14, color="#FFD700", weight="w500")], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5), padding=ft.padding.only(bottom=20)),
                    ft.Container(content=ft.Column([name, amount, category, ft.ElevatedButton("إضافة مصروف", on_click=add_expense, bgcolor="#FFD700", color="black", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), height=45)], spacing=15), bgcolor="#00000080", padding=20, border_radius=20, border=ft.border.all(1, "#FFFFFF4D")),
                    ft.Container(height=15),
                    ft.Text("المصروفات الأخيرة:", size=18, color="white", weight="bold"),
                    expenses_list,
                ], scroll=ft.ScrollMode.AUTO),
                padding=20,
                expand=True
            )
        ], expand=True)
    )

ft.app(target=main, assets_dir="assets")