from tkinter import *
from tkinter import ttk

class main_form():
    def __init__(self):
        root = Tk()
        root.title("Мое приложение")
        root.geometry("800x600")

        # Создание основного контейнера для вкладок
        self.tab_container = ttk.Notebook(root)
        self.tab_container.pack(fill="both", expand=True)

        # Создание первой вкладки
        self.tab1 = ttk.Frame(self.tab_container)
        self.tab_container.add(self.tab1, text="Генератор Дата сета")

        self.list1 = Listbox(self.tab1)
        self.list1.grid(row=0, column=0, padx=10, pady=10)

        self.image = PhotoImage(file="")  # Замените "image.png" на свой файл изображения
        self.image_label = ttk.Label(self.tab1, image=self.image)
        self.image_label.grid(row=0, column=1, padx=10, pady=10)

        self.checkbox1 = ttk.Checkbutton(self.tab1, text="Checkbox 1")
        self.checkbox1.grid(row=1, column=1, padx=10, pady=10)

        self.checkbox2 = ttk.Checkbutton(self.tab1, text="Checkbox 2")
        self.checkbox2.grid(row=2, column=1, padx=10, pady=10)

        self.checkbox3 = ttk.Checkbutton(self.tab1, text="Checkbox 3")
        self.checkbox3.grid(row=3, column=1, padx=10, pady=10)
        self.output_text = Text(self.tab1)
        self.output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        list2 = Listbox(self.tab1)
        list2.grid(row=1, column=0,rowspan=3, padx=10, pady=10)

        # Создание второй вкладки
        self.tab2 = ttk.Frame(self.tab_container)
        self.tab_container.add(self.tab2, text="Обучение модели")

        listbox = Listbox(self.tab2)
        listbox.grid(row=0, column=0, padx=10, pady=10)

        checkbox1 = ttk.Checkbutton(self.tab2, text="Флажок 1")
        checkbox1.grid(row=1, column=0, padx=10, pady=10)

        checkbox2 = ttk.Checkbutton(self.tab2, text="Флажок 2")
        checkbox2.grid(row=2, column=0, padx=10, pady=10)

        checkbox3 = ttk.Checkbutton(self.tab2, text="Флажок 3")
        checkbox3.grid(row=3, column=0, padx=10, pady=10)

        output_text = Text(self.tab2)
        output_text.grid(row=4, column=0, padx=10, pady=10)

        # Создание третьей вкладки
        self.tab3 = ttk.Frame(self.tab_container)
        self.tab_container.add(self.tab3, text="Проверка")

        listbox = Listbox(self.tab3)
        listbox.grid(row=0, column=0, padx=10, pady=10)

        image = PhotoImage(file="")
        image_label = ttk.Label(self.tab3, image=image)
        image_label.grid(row=0, column=1, padx=10, pady=10)

        listbox_bottom = Listbox(self.tab3)
        listbox_bottom.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        output_text = Text(self.tab3)
        output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        root.mainloop()


