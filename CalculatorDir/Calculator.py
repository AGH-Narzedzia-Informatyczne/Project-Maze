from tkinter import *
from CalculatorDir import Rational
from PIL import  Image,ImageTk


operators = {"+", "-", "*", "/"}
numbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}
legal_sings = operators.union(numbers)
legal_sings = legal_sings.union({"."})


def is_valid(list_of_formulas):  # sprawdza czy użytkownik nie podał błędnych znaków
    for word in list_of_formulas:
        for letter in word:
            if letter not in legal_sings:
                return False
    return True


def split_sentence(sentence):    # rozdziela dane na znaki i liczby tz 1+22 => 1, +, 22
    formulas = []
    index = 0
    last_sing_index = -1
    for letter in sentence:
        if letter in operators:
            formulas.append(sentence[last_sing_index+1:index])
            formulas.append(sentence[index:index+1])
            last_sing_index = index
        index += 1
    formulas.append(sentence[last_sing_index+1:])

    while "" in formulas:
        formulas.remove("")
    print(formulas)  # debug
    return formulas


def remove_unwanted_sings(list_of_formulas):
    # removing sings from front
    have_minus_in_front = False
    while list_of_formulas[0] in operators:  # usuwa niepotrzebne znaki z początku
        if list_of_formulas[0] == "-":
            have_minus_in_front = True
        list_of_formulas.pop(0)
    if have_minus_in_front:
        list_of_formulas.insert(0, "-")  # jeśli na początku był minus to dodaje 0-...
        list_of_formulas.insert(0, "0")

    # removing sings from end
    while list_of_formulas[-1] in operators:     # usuwa niepotrzebne znaki z końca
        list_of_formulas.pop()

    return list_of_formulas


def simple_calc(a, operator, b): # potrafi wykonać bazowe obliczenia jak 1+3
    if operator == "+":
        return a+b
    if operator == "-":
        return a-b
    if operator == "*":
        return a*b
    if operator == "/":
        return a/b
    print("Error in simple_calc")
    return 0


def priority_calc(operators_set, formulas):  # wykonuje działania na operatorach danych w operators_set
    sth_changed = False
    i = 0
    while i < len(formulas):
        if formulas[i] in operators_set:
            result = simple_calc(formulas[i - 1], formulas[i], formulas[i + 1])
            formulas.pop(i + 1)
            formulas.pop(i)
            formulas.pop(i - 1)
            formulas.insert(i - 1, result)
            sth_changed = True
            break
        i += 1
    return formulas, sth_changed


def convert_to_rational(formulas):
    print(formulas)
    rationals = []
    for word in formulas:
        if word[0] not in operators:
            rationals.append(Rational.to_rational(word))
        else:
            rationals.append(word)
    return rationals


def two_operators(sign):
    if sign == "+":
        return "-"
    if sign == "-":
        return "+"

def nawiasy_bledy(dzialanie):
    if dzialanie.find("(") != -1 or dzialanie.find(")") != -1:
        if dzialanie.count("(") != dzialanie.count(")"):
            return True
        if dzialanie.find("(") > dzialanie.find(")"):
            return True

    return False

historia = [""]
i = 0
j = 0

def hist_add(dzialanie):
    global i
    global j
    historia[i]=dzialanie
    historia.append("")
    i=i+1
    j=i

class Calculator:

    final_fraction = None

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.master.title("Kalkulator")
        #self.master.geometry("500x500")
        self.frame = Frame(self.master)
        self.master.iconbitmap(r'Images\calculator-icon.ico')
        self.kasuj = ImageTk.PhotoImage(Image.open(r'Images\kasuj.png'))

        sk = 7   # szerokosc przyciskow
        wk = 3    # wysokosc przyciskow

        self.entry = Entry(self.master)
        self.entry.grid(row=0, column=0, columnspan=4, sticky=N+S+W+E)

        self.calculate = Button(self.master, text="=", height=wk, width=sk, command=self.calculate)
        self.calculate.grid(row=6, column=3, rowspan=2)

        self.result = Entry(self.master, text="0")
        self.result.grid(row=1, column=0, columnspan=4, sticky=N+S+W+E)

        self.quitButton = Button(self.master, text='X', command=self.close_windows, bg="DarkRed", width=sk, height=wk)
        self.quitButton.grid(row=0, column=4, rowspan=2, sticky=N+S)

        self.nineButton = Button(self.master, text='9', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('9'))
        self.nineButton.grid(row=3, column=0)

        self.eightButton = Button(self.master, text='8', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('8'))
        self.eightButton.grid(row=3, column=1)

        self.sevenButton = Button(self.master, text='7', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('7'))
        self.sevenButton.grid(row=3, column=2)

        self.divisionButton = Button(self.master, text='/', height=wk, width=sk, command=lambda: self.click("/"))
        self.divisionButton.grid(row=2, column=3)

        self.sixButton = Button(self.master, text='6', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('6'))
        self.sixButton.grid(row=4, column=0)

        self.fiveButton = Button(self.master, text='5', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('5'))
        self.fiveButton.grid(row=4, column=1)

        self.fourButton = Button(self.master, text='4', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('4'))
        self.fourButton.grid(row=4, column=2)

        self.multiplicationButton = Button(self.master, text='*', height=wk, width=sk, command=lambda: self.click("*"))
        self.multiplicationButton.grid(row=3, column=3)

        self.treeButton = Button(self.master, text='3', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('3'))
        self.treeButton.grid(row=5, column=0)

        self.twoButton = Button(self.master, text='2', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('2'))
        self.twoButton.grid(row=5, column=1)

        self.oneButton = Button(self.master, text='1', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('1'))
        self.oneButton.grid(row=5, column=2)

        self.subtractionButton = Button(self.master, text='-', height=wk, width=sk, command=lambda: self.click("-"))
        self.subtractionButton.grid(row=4, column=3)

        self.clearButton = Button(self.master, text='C', height=wk, width=sk, command=self.clear)
        self.clearButton.grid(row=6, column=0)

        self.zeroButton = Button(self.master, text='0', height=wk, width=sk, bg="LightBlue", command=lambda: self.click('0'))
        self.zeroButton.grid(row=6, column=1)

        self.dotButton = Button(self.master, text='.', height=wk, width=sk, command=lambda: self.click("."))
        self.dotButton.grid(row=6, column=2)

        self.additionButton = Button(self.master, text='+', height=wk, width=sk, command=lambda: self.click("+"))
        self.additionButton.grid(row=5, column=3)

        self.additionButton = Button(self.master, text='(', height=wk, width=sk, command=lambda: self.click("("))
        self.additionButton.grid(row=2, column=0)

        self.additionButton = Button(self.master, text=')', height=wk, width=sk, command=lambda: self.click(")"))
        self.additionButton.grid(row=2, column=1)

        self.additionButton = Button(self.master, image=self.kasuj, height=wk, width=sk, command=self.dele)
        self.additionButton.grid(row=2, column=2, sticky=N+S+W+E)

        self.additionButton = Button(self.master, text='^', height=wk, width=sk, command=lambda: self.hist("-"))
        self.additionButton.grid(row=2, column=4)

        self.additionButton = Button(self.master, text='v', height=wk, width=sk, command=lambda: self.hist("+"))
        self.additionButton.grid(row=3, column=4)

        self.additionButton = Button(self.master, text='', height=wk, width=sk)
        self.additionButton.grid(row=4, column=4)

        self.additionButton = Button(self.master, text='', height=wk, width=sk)
        self.additionButton.grid(row=5, column=4)

        self.additionButton = Button(self.master, text='<=>', height=wk, width=sk, command=self.expand)
        self.additionButton.grid(row=6, column=4)

        self.result.delete(0, "end")

    def hist(self, znak):
        global j
        global i
        if i != 0:
            if znak == "-" and j > 0:
                j=j-1
            if znak == "+" and j < i:
                j=j+1
            self.entry.delete(0, 'end')
            self.entry.insert(0, historia[j])

    def dele(self):
        current = self.entry.get()
        self.entry.delete(0, 'end')
        self.entry.insert(0, current[0:len(current)-1])

    def clear(self):             # komenda czyszczenia
        self.entry.delete(0, 'end')
        self.result.delete(0, 'end')

    def close_windows(self):    # komenda zamykania
        self.master.destroy()

    def click(self, nmbr):  # wypisywanie cyfr po kliknieciu przycisku

        if self.entry.get() == '0':
            if nmbr != '+' and nmbr != '-' and nmbr != '*' and nmbr != '/' and nmbr != '.':
                self.entry.delete(0, 'end')

        self.result.delete(0, 'end')
        current = self.entry.get()
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(current) + str(nmbr))

        if len(self.entry.get()) == 1:
            if nmbr == '+' or nmbr == '-' or nmbr == '*' or nmbr == '/' or nmbr == '.':
                self.entry.delete(0, 'end')

        if len(self.entry.get()) > 2:
            current = self.entry.get()
            if current[-2] == '+' or current[-2] == '-' or current[-2] == '*' or current[-2] == '/' or current[-2] == '.':
                if current[-1] == '+' or current[-1] == '-' or current[-1] == '*' or current[-1] == '/' or current[-1] == '.':
                    self.entry.delete(0, 'end')
                    self.entry.insert(0, current[0:-2] + nmbr)

    def calculate(self):
        if len(self.entry.get()) == 0 or nawiasy_bledy(self.entry.get()):
            self.result.insert(0, "Error")
            return
        input_save = self.entry.get()

        for i in range(0, self.entry.get().count("(")+1):
            a = ""
            b = ""

            if self.entry.get().count("(") != 0:  # nawiasy
                curr = self.entry.get()
                a = curr[0: curr.index("(")]
                x = curr[curr.index("(") + 1: curr.index(")")]
                b = curr[curr.index(")") + 1:]

                while x.count("(") != 0:
                    a = a + '(' + x[:x.index("(")]
                    x = x[x.index("(") + 1:]

                self.entry.delete(0, 'end')
                self.entry.insert(0, x)

            self.result.delete(0, 'end')
            formulas = split_sentence(self.entry.get())
            formulas = remove_unwanted_sings(formulas)

            if not is_valid(formulas):
                self.result.insert(0, "Error")
                return

            formulas = convert_to_rational(formulas)
            print(formulas)

            should_continue = True
            while should_continue:
                formulas, should_continue = priority_calc({"*", "/"}, formulas)
            should_continue = True
            while should_continue:
                formulas, should_continue = priority_calc({"+", "-"}, formulas)

            print(formulas)
            result = formulas[0]
            self.final_fraction = result

            self.entry.delete(0, 'end')
            self.entry.insert(0, str(result))
            cur = self.entry.get()

            if cur[0] == "-" and len(a) != 0:
                a = a[:-1] + two_operators(a[-1])
                cur = cur[1:]

            self.entry.delete(0, 'end')
            self.entry.insert(0, str(a) + str(cur) + str(b))

        self.result.insert(0, self.show_result(self.final_fraction))
        self.entry.delete(0, 'end')

        hist_add(input_save)

    def expand(self):
        if self.result.get().find("/") == -1:
            self.result.delete(0, 'end')
            self.result.insert(0,self.show_result(self.final_fraction, "S"))
        else:
            self.result.delete(0, 'end')
            self.result.insert(0, self.show_result(self.final_fraction, "D"))


    def show_result(self, fraction, mode="S"):  # "S" for Symbolic and "D" for Decimal
        if fraction.d == 0:
            return "Div by 0 Error"
        if mode == "D":
            return fraction.n/fraction.d
        elif fraction.d == 1:
            return fraction.n
        else:
            return fraction



