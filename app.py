import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Для использования Treeview и стилей
import sqlite3
from contextlib import closing

# Функция для входа
def login():
    username = entry_username.get()
    password = entry_password.get()

    with closing(sqlite3.connect('clinic.db', timeout=10)) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
                    window.destroy()  # Закрываем окно входа
                    open_main_app(username)  # Открываем основное окно приложения с доступом, зависящим от роли
                else:
                    messagebox.showerror("Ошибка", "Неверный логин или пароль")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Ошибка базы данных", str(e))

# Функция выхода
def quit_app():
    window.quit()

# Открытие основного окна приложения с выводом списка пациентов
def open_main_app(username):
    main_app_window = tk.Tk()
    main_app_window.title("Приложение - Список пациентов")
    main_app_window.geometry("1000x600")

    # Стилизация
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#007bff", foreground="white")
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25, background="#f5f5f5", foreground="#333", fieldbackground="#f5f5f5")
    style.map("Treeview", background=[('selected', '#007bff')], foreground=[('selected', 'white')])

    # Заголовок приложения
    title_label = ttk.Label(main_app_window, text="Список пациентов", font=("Helvetica", 16, "bold"), foreground="#333", background="#f0f4f7")
    title_label.pack(pady=10)

    # Создаем Treeview для отображения данных пациентов
    columns = ("id", "client_name", "doctor", "appointment_time", "email", "phone", "address", "policy", "snils", "diagnosis")
    patient_tree = ttk.Treeview(main_app_window, columns=columns, show="headings")
    patient_tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Настраиваем заголовки для столбцов
    patient_tree.heading("id", text="ID")
    patient_tree.heading("client_name", text="Имя пациента")
    patient_tree.heading("doctor", text="Врач")
    patient_tree.heading("appointment_time", text="Дата и время")
    patient_tree.heading("email", text="Email")
    patient_tree.heading("phone", text="Телефон")
    patient_tree.heading("address", text="Адрес")
    patient_tree.heading("policy", text="Полис")
    patient_tree.heading("snils", text="СНИЛС")
    patient_tree.heading("diagnosis", text="Диагноз")

    # Настраиваем ширину столбцов
    for col in columns:
        patient_tree.column(col, width=120)

    # Загрузка данных пациентов из базы данных
    load_patients(patient_tree)

    # Кнопка для обновления данных
    refresh_button = ttk.Button(main_app_window, text="Обновить данные", command=lambda: load_patients(patient_tree))
    refresh_button.pack(pady=10)

    # Кнопка для удаления пациентов (только для админа)
    if username == 'admin':
        delete_button = ttk.Button(main_app_window, text="Удалить выбранного пациента", command=lambda: delete_patient(patient_tree))
        delete_button.pack(pady=10)
    else:
        diagnose_button = ttk.Button(main_app_window, text="Поставить диагноз", command=lambda: set_diagnosis(patient_tree, username))
        diagnose_button.pack(pady=10)

    # Кнопка для выхода из приложения
    button_quit_main = ttk.Button(main_app_window, text="Выход", command=main_app_window.quit)
    button_quit_main.pack(pady=10)

    main_app_window.mainloop()

# Функция для загрузки данных пациентов в Treeview
def load_patients(tree):
    with closing(sqlite3.connect('database.sqlite', timeout=10)) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute('SELECT id, client_name, doctor, appointment_time, email, phone, address, policy, snils, diagnosis FROM appointments')
                patients = cursor.fetchall()

                # Очистка Treeview перед добавлением новых данных
                for row in tree.get_children():
                    tree.delete(row)

                # Добавляем данные пациентов в Treeview
                for patient in patients:
                    tree.insert('', tk.END, values=patient)

            except sqlite3.OperationalError as e:
                messagebox.showerror("Ошибка базы данных", str(e))

# Функция для удаления выбранного пациента (только для админа)
def delete_patient(tree):
    selected_item = tree.selection()
    if selected_item:
        # Получаем ID выбранного пациента
        patient_id = tree.item(selected_item)['values'][0]
        
        # Подтверждение удаления
        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить пациента с ID {patient_id}?")
        
        if confirm:
            with closing(sqlite3.connect('database.sqlite', timeout=10)) as conn:
                with closing(conn.cursor()) as cursor:
                    try:
                        cursor.execute('DELETE FROM appointments WHERE id = ?', (patient_id,))
                        conn.commit()  # Фиксация изменений в базе данных
                        
                        # Удаление пациента из Treeview
                        tree.delete(selected_item)
                        
                        messagebox.showinfo("Успех", "Пациент успешно удален!")
                    except sqlite3.OperationalError as e:
                        messagebox.showerror("Ошибка базы данных", str(e))
    else:
        messagebox.showerror("Ошибка", "Не выбран пациент для удаления.")

# Функция для установки диагноза (только для врачей)
def set_diagnosis(tree, doctor_username):
    selected_item = tree.selection()
    if selected_item:
        patient_id = tree.item(selected_item)['values'][0]
        
        # Окно для выбора диагноза
        diagnosis_window = tk.Toplevel()
        diagnosis_window.title("Поставить диагноз")

        label = ttk.Label(diagnosis_window, text="Выберите диагноз:", font=("Helvetica", 12))
        label.pack(pady=10)

        # Выпадающий список для выбора диагноза
        diagnosis_combo = ttk.Combobox(diagnosis_window, font=("Helvetica", 12))

        # Загрузка диагнозов из базы данных clinic.db
        with closing(sqlite3.connect('clinic.db', timeout=10)) as conn:
            with closing(conn.cursor()) as cursor:
                try:
                    cursor.execute("SELECT diagnosis FROM diagnosis")
                    diagnoses = [row[0] for row in cursor.fetchall()]
                    if diagnoses:
                        diagnosis_combo['values'] = diagnoses  # Установка значений для выпадающего списка
                    else:
                        messagebox.showerror("Ошибка", "Нет доступных диагнозов.")
                except sqlite3.OperationalError as e:
                    messagebox.showerror("Ошибка базы данных", str(e))

        diagnosis_combo.pack(pady=10)

        # Кнопка для назначения диагноза
        def assign_diagnosis():
            selected_diagnosis = diagnosis_combo.get()
            if selected_diagnosis:
                with closing(sqlite3.connect('database.sqlite', timeout=10)) as conn:
                    with closing(conn.cursor()) as cursor:
                        cursor.execute('''
                            UPDATE appointments 
                            SET diagnosis = ? 
                            WHERE id = ?
                        ''', (selected_diagnosis, patient_id))
                        conn.commit()
                # Обновляем интерфейс после установки диагноза
                load_patients(tree)
                messagebox.showinfo("Успех", "Диагноз успешно установлен!")
                diagnosis_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Выберите диагноз!")

        assign_button = ttk.Button(diagnosis_window, text="Поставить диагноз", command=assign_diagnosis)
        assign_button.pack(pady=10)

    else:
        messagebox.showerror("Ошибка", "Не выбран пациент для назначения диагноза.")

# Создание главного окна входа
window = tk.Tk()
window.title("Вход в систему")

# Увеличение окна
window.geometry("400x300")

# Метки и поля ввода
label_username = ttk.Label(window, text="Логин", font=("Helvetica", 12))
label_username.pack(pady=10)

entry_username = ttk.Entry(window, font=("Helvetica", 12))
entry_username.pack(pady=5)

label_password = ttk.Label(window, text="Пароль", font=("Helvetica", 12))
label_password.pack(pady=10)

entry_password = ttk.Entry(window, show="*", font=("Helvetica", 12))
entry_password.pack(pady=5)

# Кнопки
button_login = ttk.Button(window, text="Войти", command=login)
button_login.pack(pady=10)

button_quit = ttk.Button(window, text="Выход", command=quit_app)
button_quit.pack(pady=5)

# Запуск окна входа
window.mainloop()
