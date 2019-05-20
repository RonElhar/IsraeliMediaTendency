import operator
from tkinter import *
from tkinter.ttk import *
from parties_dictionary import *
from backend import *


# Dictionary window implementation
def open_dictionary():
    def chose_word():
        similar_text.set(listbox.get(listbox.curselection()))
        print(similar_text.get())
        dictionary_window.destroy()

    def chose_party(var, *args):
        listbox.delete(0, END)
        for word in parties_vocab[dict_var.get()]:
            listbox.insert(END, word)

    dictionary_window = Tk()
    dict_var = StringVar(dictionary_window)
    dict_var.set(choices[0])
    dict_var.trace_variable('w', chose_party)
    party_c = Combobox(master=dictionary_window, values=choices, textvariable=dict_var)
    choose_b = Button(master=dictionary_window, text="Choose", command=chose_word)
    dict_frame = Frame(dictionary_window)
    listbox = Listbox(master=dict_frame, width=40, height=20)
    for word in parties_vocab[dict_var.get()]:
        listbox.insert(END, word)
    listbox.pack(side="left", fill="y")
    dict_scroll = Scrollbar(dict_frame, orient="vertical")
    dict_scroll.config(command=listbox.yview)
    dict_scroll.pack(side="right", fill="y")
    dict_variable = StringVar(dictionary_window)
    dict_variable.set(choices[0])
    party_c.pack()
    dict_frame.pack()
    choose_b.pack()
    dictionary_window.mainloop()


# Event for choosing different site
def chose_site(var, *args):
    print(site_variable.get())
    load_model(site_variable.get(), period_variable.get().replace(' ', ''))


def chose_period(var, *args):
    print(period_variable.get())
    load_model(site_variable.get(), period_variable.get().replace(' ', ''))


# Event handler for showing similar words for the input text
def show_similar():
    similar = get_sentence_similarity(similar_text.get())
    text_box.config(state=NORMAL)
    text_box.delete('1.0', END)
    i = 1
    text_box.insert(END, 'Showing similar words for \'' + similar_text.get() + '\':\n')
    for word in similar:
        text_box.insert(END, str(i) + '. ' + word + '\n')
        i += 1
    text_box.config(state=DISABLED)


# Event handler for showing relations of a party
def show_relations():
    relations = get_relations(party_variable.get())
    parties = sorted(relations.items(), key=operator.itemgetter(1), reverse=True)
    text_box.config(state=NORMAL)
    text_box.delete('1.0', END)
    text_box.insert(END, 'Showing \'' + party_variable.get() + '\' relations to other parties\n')
    i = 1
    for t in parties:
        text_box.insert(END, str(i) + '. ' + t[0] + '\n')
        i += 1
    text_box.config(state=DISABLED)


'''
Initialize main window
'''
root = Tk()

choices = list(parties_vocab.keys())

site_choices = ["ynet"]
site_variable = StringVar(root)
site_variable.set(site_choices[0])
site_variable.trace_variable('w', chose_site)
choose_site_c = Combobox(master=root, values=site_choices, textvariable=site_variable)

period_choices = ["Elections Period", "All Time"]
period_variable = StringVar(root)
period_variable.set(period_choices[0])
period_variable.trace_variable('w', chose_period)
choose_period_c = Combobox(master=root, values=period_choices, textvariable=period_variable)

party_variable = StringVar(root)
party_variable.set(choices[0])
choose_party_c = Combobox(master=root, values=choices, textvariable=party_variable)
show_relations_b = Button(master=root, text="View Relations", command=show_relations)

similar_text = StringVar()
similar_words_e = Entry(master=root, width=22, textvariable=similar_text)
similar_words_b = Button(master=root, text="View Similar", command=show_similar)
choose_from_dict_b = Button(master=root, text="Choose From Elections dictionary", command=open_dictionary)

frame = Frame(root)
text_box = Text(master=frame, width=40, state=DISABLED)
text_box.pack(side="left", fill="y")
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=text_box.yview)
scrollbar.pack(side="right", fill="y")

Label(master=root, text="Choose Site").grid(row=0, column=0)
choose_site_c.grid(row=0, column=1)

Label(master=root, text="Choose Period").grid(row=1, column=0)
choose_period_c.grid(row=1, column=1)

Label(master=root, text="~~~~~~~~~~~~~Parties Relations Feature~~~~~~~~~~~~~").grid(row=2, columnspan=3)
Label(master=root, text="Choose Party").grid(row=3, column=0)
choose_party_c.grid(row=3, column=1)
show_relations_b.grid(row=3, column=2)

Label(master=root, text="~~~~~~~~~~~~~Similar Words Feature~~~~~~~~~~~~~~~").grid(row=4, columnspan=3)
Label(master=root, text="Free Text").grid(row=5, column=0)
similar_words_e.grid(row=5, column=1)
similar_words_b.grid(row=5, column=2, rowspan=2)
Label(master=root, text="OR").grid(row=6, column=0)
choose_from_dict_b.grid(row=6, column=1, columnspan=1)

Label(master=root, text="Results:").grid(row=7, column=0)
frame.grid(row=8, column=0, rowspan=3, columnspan=3)

if __name__ == '__main__':
    load_model(site_variable.get(), period_variable.get().replace(' ', ''))
    root.mainloop()
