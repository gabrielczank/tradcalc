import yaml
import customtkinter
import tkinter
import os
from PIL import ImageTk, Image# para o ícone
import pyperclip
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# TODO: colocar pra ler o arquivo de textos correto dependendo do idioma da pessoa
# TODO: deixar os presets separado pra cada aba, para evitar conflito

# inter = None não sei é necessário ter esta variável vazia

# config de idioma
with open('config.yml', 'r') as f:
    lang = yaml.load(f.read(), Loader=yaml.Loader)

with open(f"lang/{lang['lang']}.yaml", "r", encoding='utf-8') as f:
    inter = yaml.load(f.read(), Loader=yaml.Loader)

# print(inter)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        strvar = customtkinter.StringVar
        self.title(inter["texts"]["calculator"])
        self.geometry("380x500")

        self.resizable(False, False)
        self.tab = customtkinter.CTkTabview(self)
        self.tab.grid(row=1, column=1, padx=40, pady=20, sticky="nw")
        self.tab.add(inter["texts"]["sheet"])
        self.tab.add(inter["texts"]["words"])
        self.tab.tab(inter["texts"]["sheet"]).grid_columnconfigure(0, weight=1)
        self.tab.tab(inter["texts"]["words"]).grid_columnconfigure(0, weight=1)

        def calc():
            """calculo de laudas usando regra de três."""
            try:
                # limpando os campos em vermelho (não vou por um if, ocupa linhas a toa)
                self.char.configure(border_color="grey")
                self.tam.configure(border_color="grey")
                self.preco.configure(border_color="grey")
                div = float(self.char.get()) / float(self.tam.get())
                # print(f'O documento possui {round(div, 2)} laudas')
                total = float(self.preco.get().replace(",", ".")) * div
                # print(f'Preço total: R${round(total, 2)}')
                self.result.configure(textvariable=strvar(value=f'{inter["texts"]["total_val"]}: {self.currency.get()} '
                                           f'{round(total, 2)} ({round(div, 2)} {inter["texts"]["sheets"]})'))

            except ValueError:
                # verificando se todos os campos estão preenchidos
                for x in [self.char, self.tam, self.preco]:
                    if x.get() == '' or x.get().isnumeric() == False:
                        x.configure(border_color="red")
                    else:
                        pass
                self.result.configure(textvariable=strvar(value=inter["errors"]["invalid_vals"]))
        # -------------------------- calculo por palavra -------------------------------------

        def calcword():
            try:
                self.prpa.configure(border_color="gray")
                self.words.configure(border_color="gray")
                total = float(self.words.get()) * float(self.prpa.get().replace(",", "."))
                self.result.configure(textvariable=strvar(value=f"{self.currency.get()} {round(total, 3)}"))
            except ValueError:
                for x in [self.prpa, self.words]:
                    if x.get() == '' or x.get().isnumeric() == False:
                        x.configure(border_color="red")
                    else:
                        pass
                self.result.configure(textvariable=strvar(value=inter["errors"]["invalid_vals"]))
        # =================apagar isso quando tiver preset funcional====================
        correct = tkinter.DoubleVar(value=1500)

        def locale(x):
            """preciso achar uma forma melhor pra isso..."""
            with open('config.yml', 'w') as f:
                newlang = [{'lang': x}]
                yaml.dump_all(newlang, f)
            with open(f"lang/{lang['lang']}.yaml", "r", encoding='utf-8') as f:
                yaml.load(f.read(), Loader=yaml.Loader)
            app.destroy()
            os.system("main.py")

        def presets(x):
            if x == "PRESET1":
                self.tam.configure(textvariable=correct, state="readonly", text_color="grey")
        # -------------------- Calculo por laudas ------------------------
        # -------------- caracteres    ------------------
        self.charlabel = customtkinter.CTkLabel(self.tab.tab(inter["texts"]["sheet"]), text=inter["texts"]["char_count"])
        self.charlabel.grid()
        self.char = customtkinter.CTkEntry(self.tab.tab(inter["texts"]["sheet"]), placeholder_text=inter["texts"]["val"])
        self.char.grid()
        # ----------------- laudas     -----------------
        self.tamlabel = customtkinter.CTkLabel(self.tab.tab(inter["texts"]["sheet"]), text=inter["texts"]["sheet_size"])
        self.tamlabel.grid()
        self.tam = customtkinter.CTkEntry(self.tab.tab(inter["texts"]["sheet"]), placeholder_text=inter["texts"]["val"])
        self.tam.grid()
        self.precolabel = customtkinter.CTkLabel(self.tab.tab(inter["texts"]["sheet"]), text=inter["texts"]["price_by_sheet"])
        self.precolabel.grid()
        self.preco = customtkinter.CTkEntry(self.tab.tab(inter["texts"]["sheet"]), placeholder_text=inter["texts"]["val"])
        self.preco.grid()
        self.calcbutton = customtkinter.CTkButton(master=self.tab.tab(inter["texts"]["sheet"]), text=inter["texts"]["compute"], command=calc)
        self.calcbutton.grid(pady=5)
        self.result = customtkinter.CTkEntry(self, state='readonly', width=280)
        self.result.grid(row=2, column=1)

        # ================================= configs ===================================
        self.options = customtkinter.CTkFrame(self, width=240)
        self.options.grid(row=3, column=1, padx=40, pady=20, sticky="nw")
        self.curlabel = customtkinter.CTkLabel(self.options, text=inter["texts"]["currency"])
        self.curlabel.grid(column=0, row=0)
        self.currency = customtkinter.CTkOptionMenu(self.options, dynamic_resizing=False,
                                                    values=["BRL", "USD", "EUR"], )
        self.currency.grid(padx=5, pady=5)
        """self.presetlab = customtkinter.CTkLabel(self.options, text="Presets")
        self.presetlab.grid(column=2, row=0)
        self.preset = customtkinter.CTkOptionMenu(self.options, dynamic_resizing=True,
                                                  values=["PRESET1", "PRESET 2"], command=presets)
        self.preset.grid(row=1, column=2, padx=5, pady=5)"""
        self.langlab = customtkinter.CTkLabel(self.options, text=inter["texts"]['language'])
        self.langlab.grid(column=2, row=0)
        self.lang = customtkinter.CTkOptionMenu(self.options, values=['en', 'br'], command=locale)
        self.lang.set(inter['texts']['select'])
        self.lang.grid(row=1, column=2, padx=5, pady=5)
        # ------------------------- Calculo por palavras ----------------------
        self.wordslabel = customtkinter.CTkLabel(self.tab.tab(inter["texts"]["words"]), text=inter["texts"]["word_count"])
        self.wordslabel.grid()
        self.words = customtkinter.CTkEntry(self.tab.tab(inter["texts"]["words"]), placeholder_text=inter["texts"]["val"])
        self.words.grid()
        self.prpalabel = customtkinter.CTkLabel(self.tab.tab(inter["texts"]["words"]), text=inter["texts"]["price_by_word"])
        self.prpalabel.grid()
        self.prpa = customtkinter.CTkEntry(self.tab.tab(inter["texts"]["words"]), placeholder_text=inter["texts"]["val"])
        self.prpa.grid()
        self.prpabutton = customtkinter.CTkButton(self.tab.tab(inter["texts"]["words"]), text=inter["texts"]["compute"],
                                                  command=calcword)
        self.prpabutton.grid(pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
