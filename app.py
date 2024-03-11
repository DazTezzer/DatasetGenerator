from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os


def show_info(list,info_label):
    print("bruh")
    selected_index = list.curselection()
    print(selected_index)
    if selected_index:
        selected_item = list.get(selected_index)
        info_text = f"Название: {selected_item}\n"
        info_label.config(state='normal')
        info_label.insert(END, info_text)
        info_label.config(state='disabled')
def set_list(list):
    path = browseFiles()
    files = [f for f in os.listdir(path) if f.endswith('.png')]
    list.delete(0, END)
    for file in files:
        list.insert(END, file)
def browseFiles():
    path = filedialog.askdirectory(title="Выберите папку с файлами PNG")
    return path
class main_form():
    def __init__(self):
        root = Tk()
        root.title("Мое приложение")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")

        # Создание основного контейнера для вкладок
        self.tab_container = ttk.Notebook(root)
        self.tab_container.pack(fill="both", expand=True)

        # Создание первой вкладки
        self.tab1 = ttk.Frame(self.tab_container)
        self.tab_container.add(self.tab1, text="Генератор Дата сета")

        self.output_text = Text(self.tab1)
        self.output_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        scrollbar = Scrollbar(self.tab1, command=self.output_text.yview)
        scrollbar.grid(row=7, column=2, sticky='ns')
        self.output_text.config(yscrollcommand=scrollbar.set)

        self.output_text.config(state='disable')

        self.list1 = Listbox(self.tab1)
        self.list1.grid(row=0, column=0, padx=10, pady=10)
        self.list1.bind("<ButtonRelease-1>", lambda event: show_info(self.list1, self.output_text))

        self.button_explore1 = Button(self.tab1,text="Browse Files",command=lambda:set_list(self.list1))
        self.button_explore1.grid(row=1, column=0, padx=10, pady=10)

        self.list2 = Listbox(self.tab1)
        self.list2.grid(row=2, column=0, padx=10, pady=10)
        self.list2.bind("<ButtonRelease-1>", lambda event: show_info(self.list2, self.output_text))

        self.button_explore2 = Button(self.tab1, text="Browse Files", command=lambda: set_list(self.list2))
        self.button_explore2.grid(row=6, column=0, padx=10, pady=10)

        self.image = PhotoImage(file="1.png")  # Замените "image.png" на свой файл изображения

        self.image_label = ttk.Label(self.tab1, image=self.image)
        self.image_label.grid(row=0, column=1,rowspan=8, padx=10, pady=10)

        self.checkbox1 = ttk.Checkbutton(self.tab1, text="Checkbox 1")
        self.checkbox1.grid(row=1, column=1, padx=10, pady=10)

        self.checkbox2 = ttk.Checkbutton(self.tab1, text="Checkbox 2")
        self.checkbox2.grid(row=2, column=1, padx=10, pady=10)

        self.checkbox3 = ttk.Checkbutton(self.tab1, text="Checkbox 3")
        self.checkbox3.grid(row=3, column=1, padx=10, pady=10)




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


