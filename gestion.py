from tkinter import *
from tkinter import colorchooser
import sqlite3
import matplotlib.pyplot as plt
# hashlib pour hasher les mdp

screen = Tk()

user_dict = {}

is_draw = False
btn_look = None
btn_quit = None

conn = sqlite3.connect('userdb.db')
cur = conn.cursor()

screen.title("PiggyBank")
screen.geometry("1080x800")
screen.minsize(500, 450)
screen.config(background="#884EA0")
screen.iconbitmap('assets/logo.ico')

def error_tirelire(message):
    global label_error

    try:
        label_error.destroy()
    except:
        pass

    label_error = Label(screen, text=message, font=("Arial", 35),
                        bg=user_dict['color'][0], fg="red")
    label_error.pack(side=BOTTOM)

    label_error.after(3000, label_error.destroy)

def Btn_App():
    global frame2

    frame2 = Frame(screen, bg=user_dict['color'][0])
    frame2.pack(side=TOP, fill=X)
    btn_app = Button(frame2, text="menu", command=app, font=("Arial", 25), bg="#212F3C", fg="#D35400")

    btn_app.pack(side=LEFT, pady=25, padx=50)

def check_username():
    global frame

    frame = Frame(screen, bg="#884EA0")

    frame.pack(expand=YES, fill=Y)

    label_un_pw = Label(frame, text="connectez-vous à votre compte", font=("Arial", 35), bg="#884EA0", fg="white")
    entry_username = Entry(frame, font=50)
    entry_password = Entry(frame, font=50)
    label_username = Label(frame, text="entrez votre identifiant", font=("Arial", 25), bg="#884EA0", fg="black")
    label_password = Label(frame, text="entrez votre mot de passe", font=("Arial", 25), bg="#884EA0", fg="black")
    button_validation = Button(frame, command=lambda: into_check_username(entry_username.get(), entry_password.get()), text="se connecter", font=("Arial", 30), bg="black",
                               fg="#884EA0")

    label_un_pw.grid(row=0, column=0, pady=25)
    label_username.grid(row=1, column=0, pady=15)
    entry_username.grid(row=2, column=0, pady=15)
    label_password.grid(row=3, column=0, pady=15)
    entry_password.grid(row=4, column=0, pady=15)
    button_validation.grid(row=5, column=0, pady=25)

    entry_password.bind('<Return>', lambda e: into_check_username(entry_username.get(), entry_password.get()))
    entry_username.bind('<Return>', lambda e: into_check_username(entry_username.get(), entry_password.get()))

def into_check_username(username, password):
    global user_dict

    user_table_db = cur.execute("SELECT id, username, password, money, color, listValue FROM User WHERE username = ? AND password = ?", (username, password))
    user_table = user_table_db.fetchall()
    print(user_table)

    if user_table != []:
        user_dict['id'] = user_table[0][0]
        user_dict['username']= user_table[0][1]
        user_dict['password']= user_table[0][2]
        user_dict['money']= user_table[0][3]
        user_dict['color'] = tuple(user_table[0][4].split(",", 1))

        try :
            user_dict['list_value'] = list(user_table[0][5].split(",", len(user_table[0][5])))
            for i in range(len(user_dict['list_value'])):
                user_dict['list_value'][i] = float(user_dict['list_value'][i])
                print('alright')
        except IndexError:
            print('error')
            user_dict["list_value"] = [user_dict["money"]]

        print(user_dict)

        screen.config(background=user_dict['color'][0])

        app()
    
    else:
        error_tirelire('Identifiant ou mot de passe incorrect')

def add():
    global ajouts_Entry, frame

    Reset_screen()

    Btn_App()

    frame = Frame(screen, bg=user_dict["color"][0])
    frame.pack(expand=YES, fill=Y)

    Label_ajouts = Label(frame, text="Entrez la valeur que vous voulez ajouter", font=("Arial", 30), bg=user_dict["color"][0], fg="black")
    ajouts_Entry = Entry(frame, font=50)
    btn_add = Button(frame, text="ajouter", command=lambda: into_add(ajouts_Entry.get()), font=("Arial", 25), bg=user_dict["color"][1], fg=user_dict["color"][0])

    Label_ajouts.grid(row=0, column=0, pady=25)
    ajouts_Entry.grid(row=1, column=0, pady=25)
    btn_add.grid(row=2, column=0, pady=25)

def into_add(entry_ajouts):
    try:
        entry_ajouts = float(entry_ajouts)
        user_dict['money'] += entry_ajouts
        app()

    except ValueError:
        error_tirelire('Veuillez entrer un nombre.')

def soustraire():
    global frame

    Reset_screen()

    Btn_App()

    frame = Frame(screen, bg=user_dict["color"][0])
    frame.pack(expand=YES, fill=Y)

    label_retire = Label(frame, text="Entrez la valeur que vous voulez retirer", font=("Arial", 30), bg=user_dict["color"][0], fg="black")
    soustraire_Entry = Entry(frame, font=50)
    btn_soustraire = Button(frame, command=lambda: into_soustraire(soustraire_Entry.get()), text="retirer", font=("Arial", 25), bg=user_dict["color"][1], fg=user_dict["color"][0])

    label_retire.grid(row=0, column=0, pady=25)
    soustraire_Entry.grid(row=1, column=0, pady=25)
    btn_soustraire.grid(row=2, column=0, pady=25)

def into_soustraire(retire):

    try:
        retire = float(retire)

        if retire > user_dict['money']:
            error_tirelire('Vous ne pouvez retirer autant à votre tirelire')
        else:
            user_dict['money'] -= retire
            app()

    except ValueError:
        error_tirelire('Veuillez entrer un nombre')

def into_E_V_T(enter):
    try:
        enter = float(enter)
        user_dict['money'] = enter

        app()

    except ValueError:
        error_tirelire('Veuillez entrer un nombre')

def enter_valeur_tirelire():
    global frame

    Reset_screen()

    Btn_App()

    frame = Frame(screen, bg=user_dict["color"][0])
    frame.pack(expand=YES, fill=Y)

    label_enter = Label(frame, text="Entrer la nouvelle valeur de la tirelire", font=("Arial", 30), bg=user_dict["color"][0], fg='black')
    enter_Entry = Entry(frame, font=30)
    btn_enter = Button(frame, command=lambda: into_E_V_T(enter_Entry.get()), text="valider la valeur de la tirelire", font=("Arial", 25), bg=user_dict["color"][1], fg=user_dict["color"][0])

    label_enter.grid(row=0, column=0, pady=30)
    enter_Entry.grid(row=2, column=0, pady=30)
    btn_enter.grid(row=3, column=0, pady=30)

def affichage_texte():
    global i, text2
    text = f"vous avez {str(user_dict['money'])} € dans votre tirelire"
    if i < len(text):
        text2 += text[i]
        i += 1
    textvar.set(text2)
    screen.after(50, affichage_texte)

def know_valeur():
    global frame, textvar, i, text2

    Reset_screen()

    Btn_App()

    frame = Frame(screen, bg=user_dict["color"][0])
    frame.pack(expand=YES, fill=Y)
    
    textvar = StringVar()

    i = 0
    text2 = ''

    label_know = Label(frame, textvariable=textvar, font=("Arial", 45), bg=user_dict["color"][0], fg="black") 
    label_know.pack(expand=YES)

    affichage_texte()

def save_quit():
    color = f"{user_dict['color'][0]},{user_dict['color'][1]}"
    user_dict["list_value"].append(user_dict["money"])
    listValue = ""
    for elt in user_dict["list_value"]:
        listValue += str(elt) + ','
    listValue = listValue[:len(listValue)-1]
    cur.execute("UPDATE User SET money=?, color=?, listValue=? WHERE id=?", (user_dict["money"], color, listValue, user_dict["id"]))
    conn.commit()
    conn.close()
    screen.destroy()
    quit()

def Set_color1():
    user_dict['color'] = (colorchooser.askcolor()[1], user_dict["color"][1])
    print(user_dict["color"])
    screen.config(background=user_dict['color'][0])

def Set_color2():
    user_dict['color'] = (user_dict["color"][0], colorchooser.askcolor()[1])
    print(user_dict["color"])

def Looks():
    global frame

    Reset_screen()

    Btn_App()
    frame = Frame(screen, bg=user_dict['color'][0])

    frame.pack(expand=YES)

    btn_color1 = Button(frame, text='couleur 1', command=Set_color1, font=("Arial", 30), bg=user_dict["color"][0], fg="black")
    btn_color2 = Button(frame, text='couleur 2', command=Set_color2, font=("Arial", 30), bg=user_dict["color"][1], fg="black")

    btn_color1.grid(row=0, column=0, padx=15)
    btn_color2.grid(row=0, column=1, padx=15)

def Settings():
    global is_draw, btn_look, btn_quit, btn_graphic

    if btn_quit is None or btn_look is None:
        return

    if is_draw:
        btn_quit.grid_remove()
        btn_look.grid_remove()
        btn_graphic.grid_remove()
    else:
        btn_quit.grid(row=0, column=1, pady=(15, 0))
        btn_look.grid(row=1, column=1)
        btn_graphic.grid(row=2, column=1, pady=(0, 15))
    is_draw = not is_draw

def Reset_screen():
    global is_draw

    is_draw = False

    try:
        frame2.destroy()
    except:
        pass

    try:
        frame.destroy()
    except:
        pass
    
    try:
        label_error.destroy()
    except:
        pass

def Graphic():
    
    if user_dict["list_value"] != []:
        l_x = []
        l_y = []
        for i in range(len(user_dict["list_value"])):
            l_x.append(i)
            l_y.append(user_dict["list_value"][i])
    
        plt.plot(l_x, l_y, '-ob')

        plt.xlabel('historique de la tirelire')
        plt.axis((0, len(user_dict['list_value']), 0, max(user_dict['list_value'])+100))
    
        plt.show()

def app():
    global frame, frame2, btn_quit, btn_look, btn_graphic

    Reset_screen()

    frame = Frame(screen, bg=user_dict["color"][0])
    frame2 = Frame(screen, bg=user_dict["color"][0])

    frame2.pack(side=TOP, fill=X)
    frame.pack(expand=YES)

    btn_quit = Button(frame2, command=save_quit, text="Sauvegarder et quitter", font=("Arial",20), bg=user_dict["color"][1], fg=user_dict["color"][0])
    btn_look = Button(frame2, command=Looks, text="Style", font=("Arial",20), bg=user_dict["color"][1], fg=user_dict["color"][0])
    btn_graphic = Button(frame2, command=Graphic, text="analyser ma tirelire", font=("Arial",20), bg=user_dict["color"][1], fg=user_dict["color"][0])

    btn_entercontrol = Button(frame, command=enter_valeur_tirelire, text="entrer une valeur pour la tirelire", font=("Arial", 30), bg=user_dict["color"][1], fg=user_dict["color"][0])
    btn_know = Button(frame, command=know_valeur, text="voir la valeur de la tirelire", font=("Arial", 30), bg=user_dict["color"][1], fg=user_dict["color"][0])
    btn_addcontrol = Button(frame, command=add, text="ajouter de l'argent à la tirelire", font=("Arial", 30), bg=user_dict["color"][1], fg=user_dict["color"][0])
    btn_soustrairecontrol = Button(frame, command=soustraire, text="retirer de l'argent à la tirelire", font=("Arial", 30), bg=user_dict["color"][1], fg=user_dict["color"][0])
    btn_setting = Button(frame2, command=Settings, text="paramètres", font=("Arial",20), bg=user_dict["color"][1], fg=user_dict["color"][0])

    btn_setting.grid(row=0, column=0, padx=(15, 0), pady=(15, 0))
    btn_entercontrol.grid(row=0, column=0, pady=25)
    btn_know.grid(row=1, column=0, pady=25)
    btn_addcontrol.grid(row=2, column=0, pady=25)
    btn_soustrairecontrol.grid(row=3, column=0, pady=25)

# lancement de l'application

check_username()

screen.mainloop()