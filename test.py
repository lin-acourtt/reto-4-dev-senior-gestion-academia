import customtkinter

def get_selected_index(combobox):
    selected_index = combobox.current()
    print(f"Selected index: {selected_index}")

app = customtkinter.CTk()

combobox = customtkinter.CTkComboBox(master=app, values=["Item 1", "Item 2", "Item 3"], command=lambda: get_selected_index(combobox))
combobox.pack(padx=20, pady=10)
print(combobox.current())
app.mainloop()