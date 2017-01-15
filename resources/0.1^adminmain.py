

class Main(object):

    def __init__(self):
        self.epsilon = "E"

        #FA data
        self.states = []
        self.alphabet = []
        self.initial_state = ""
        self.final_states = []
        self.table = []

        #G data
        self.nonterminals = []
        self.terminals = []
        self.start = ""
        self.predicates = {}

    def read(self, what):
        if what == "FA":
            Q = input("give the states separated by , : ")
            E = input("give the alphabet : ")
            q0 = input("give the initial state: ")
            F = input("give the final state/states: ")
            s = Q.split(",")
            for state in s:
                self.states.append(state.strip())
            e = E.split(",")
            for letter in e:
                self.alphabet.append(letter.strip())
            self.initial_state = q0
            f = F.split(",")
            for f_state in f:
                self.final_states.append(f_state.strip())

            for st in range(0, len(self.states)):
                line = []
                for lt in range(0, len(self.alphabet)):
                    value = input("give transition for (" + str(self.states[st]) + ", " + str(self.alphabet[lt]) + ") : ")
                    line.append(value)
                self.table.append(line)
        if what == "G":
            N = input("give the non-terminals: ")
            T = input("give the terminals: ")
            S = input("give the start symbol: ")
            P = input("give the predicates: ")

            n = N.split(",")
            for nont in n:
                self.nonterminals.append(nont.strip())
            t = T.split(",")
            for ter in t:
                self.terminals.append(ter.strip())
            self.start = S
            P = P.split(",")
            for predicates in P:
                predicates = predicates.strip()
                values = predicates.split(" -> ")
                lhs = values[0]
                rhs = values[1].split("|")
                self.predicates[lhs] = rhs


    def display(self, from_,  what):
        if from_ == "FA":
            if what == "all":
                print("states = " + str(self.states))
                print("alphabet = " + str(self.alphabet))
                print("initial state = " + str(self.initial_state))
                print("final states = " + str(self.final_states))
                print("transitions: ")
                for line in self.table:
                    print(line)
            elif what == "states":
                print("states = " + str(self.states))
            elif what == "alphabet":
                print("alphabet = " + str(self.alphabet))
            elif what == "initial state":
                print("initial state = " + str(self.initial_state))
            elif what == "final states":
                print("final states = " + str(self.final_states))
            elif what == "transitions":
                print("transitions: ")
                for line in self.table:
                    print(line)
        elif from_ == "G":
            if what == "all":
                print("Nonterminals = " + str(self.nonterminals))
                print("Terminals = " + str(self.terminals))
                print("Start NonTerm = " + str(self.start))
                print("Predicates = " + str(self.predicates))
            elif what == "nonterminals":
                print("Nonterminals = " + str(self.nonterminals))
            elif what == "terminals":
                print("Terminals = " + str(self.terminals))
            elif what == "start":
                print("Start NonTerm = " + str(self.start))
            elif what == "predicates":
                print("Predicates = " + str(self.predicates))

    def print_menu(self):
        print("1: FA read data")
        print("2: print FA states")
        print("3: print FA alphabet")
        print("4: print FA initial state")
        print("5: print FA final states")
        print("6: print FA transitions")
        print("7: print FA all")
        print("10: G read data")
        print("11: G print nonterminals")
        print("12: G print terminals")
        print("13: G print start symbol")
        print("14: G print predicates")
        print("15: G print all")
        print("16: G check if regular")
        print("17: G to FA")
        print("18: FA to G")
        print("exit: exit")

    def check_input(self, input_sequence):
        current_state = self.initial_state
        for character in input_sequence:
            char_index = self.alphabet.index(character)
            current_state = self.table[self.states.index(current_state)][char_index]
        if self.final_states.count(current_state) > 0:
            return True
        else:
            return False

    def get_longest_sequence(self, input_sequence):
        if self.check_input(input_sequence):
            return input_sequence
        else:
            sub_string_length = 1
            longest_sub_string = ""
            while sub_string_length <= len(input_sequence):
                sub_string = input_sequence[0:sub_string_length]
                if self.check_input(sub_string):
                    longest_sub_string = sub_string
                sub_string_length += 1
            return longest_sub_string

    def check_if_regular(self):
        def is_epsilon(token):
            if token == "E":
                return True

        def is_composed(token):
            if len(token) > 2:
                return False
            return self.terminals.count(token[0]) > 0 and self.nonterminals.count(token[1]) > 0

        def is_terminal(token):
            return self.terminals.count(token) > 0

        def is_valid(list_):
            for val in list_:
                if not (is_terminal(val) or is_composed(val)):
                    return False
            return True

        def contains_start(list_):
            for elem in list_:
                for char in elem:
                    if char == self.start:
                        return True
            return False

        has_epsilon = False

        for key in self.predicates:
            for elem in self.predicates[key]:
                if is_epsilon(elem):
                    has_epsilon = True

        if has_epsilon:
            for key in self.predicates:
                if contains_start(self.predicates[key]):
                    return False

        for key in self.predicates:
            if not is_valid(self.predicates[key]):
                return False
        return True

    def g_to_fa(self):
        def is_composed(token):
            if len(token) > 2:
                return False
            return self.terminals.count(token[0]) > 0 and self.nonterminals.count(token[1]) > 0

        def is_terminal(token):
            return self.terminals.count(token) > 0

        def is_epsilon(token):
            if token == "E":
                return True

        has_epsilon = False
        for key in self.predicates:
            for elem in self.predicates[key]:
                if is_epsilon(elem):
                    has_epsilon = True

        if not self.check_if_regular():
            return False
        else:
            self.states.extend(self.nonterminals)
            self.states.append("K")
            self.initial_state = self.start
            self.alphabet = self.terminals
            self.final_states.append("K")
            if has_epsilon:
                self.final_states.append(self.initial_state)
            for state in self.predicates:
                line = ["" for _ in self.terminals]
                elems = self.predicates[state]
                for value in elems:
                    if is_terminal(value):
                        line[self.terminals.index(value[0])] += "K"
                    else:
                        if is_composed(value):
                            line[self.terminals.index(value[0])] += value[1]
                self.table.append(line)
            line = ["" for _ in self.terminals]
            self.table.append(line)

    def fa_to_g(self):
        self.nonterminals.extend(self.states)
        self.terminals.extend(self.alphabet)
        self.start = self.initial_state
        for state_index in range(0, len(self.states)):
            self.predicates[self.states[state_index]] = []
            for let_index in range(0, len(self.table[state_index])):
                self.predicates[self.states[state_index]].append(self.alphabet[let_index] + self.table[state_index][let_index])
                if self.states[state_index] == self.start:
                    self.predicates[self.states[state_index]].append(self.alphabet[let_index])

    def run(self):
        while True:
            self.print_menu()
            option = input("give your option: ")
            try:
                if option == "1":
                    self.read("FA")
                elif option == "2":
                    self.display("FA", "states")
                elif option == "3":
                    self.display("FA", "alphabet")
                elif option == "4":
                    self.display("FA", "initial state")
                elif option == "5":
                    self.display("FA", "final states")
                elif option == "6":
                    self.display("FA", "transitions")
                elif option == "7":
                    self.display("FA", "all")
                elif option == "10":
                    self.read("G")
                elif option == "11":
                    self.display("G", "nonterminals")
                elif option == "12":
                    self.display("G", "terminals")
                elif option == "13":
                    self.display("G", "start")
                elif option == "14":
                    self.display("G", "predicates")
                elif option == "15":
                    self.display("G", "all")
                elif option == "16":
                    print(self.check_if_regular())
                elif option == "17":
                    self.g_to_fa()
                    self.display("FA", "all")
                elif option == "18":
                    self.fa_to_g()
                    self.display("G", "all")
                elif option == "exit":
                    break
            except Exception as e:
                continue

if __name__ == "__main__":
    main = Main()
    main.run()






























