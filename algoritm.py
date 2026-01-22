import random
import numpy as np


class EvolutieDiferentiala:
    def __init__(self, functie_fitness, limite, dim, pop_size=20, F=0.8, CR=0.7, max_gen=50):
        self.fitness_func = functie_fitness
        self.limite = limite
        self.dim = dim
        self.pop_size = pop_size
        self.F = F
        self.CR = CR
        self.max_gen = max_gen

        self.populatie = []
        self.scoruri = []

        self.initializare()

    def initializare(self):
        self.populatie = []

        for _ in range(self.pop_size):
            ind = []
            for i in range(self.dim):
                min_val = self.limite[i][0]
                max_val = self.limite[i][1]
                valoare = random.uniform(min_val, max_val)
                ind.append(valoare)

            self.populatie.append(np.array(ind))

        self.populatie = np.array(self.populatie)

        lista_scoruri = []
        for ind in self.populatie:
            scor = self.fitness_func(ind)
            lista_scoruri.append(scor)

        self.scoruri = np.array(lista_scoruri)

    def mutatie(self, index_curent):
        indecsi_posibili = []
        for i in range(self.pop_size):
            if i != index_curent:
                indecsi_posibili.append(i)

        alesi = np.random.choice(indecsi_posibili, 3, replace=False)
        a = self.populatie[alesi[0]]
        b = self.populatie[alesi[1]]
        c = self.populatie[alesi[2]]

        vector_mutant = a + self.F * (b - c)

        for k in range(self.dim):
            limita_min = self.limite[k][0]
            limita_max = self.limite[k][1]

            if vector_mutant[k] < limita_min:
                vector_mutant[k] = limita_min

            if vector_mutant[k] > limita_max:
                vector_mutant[k] = limita_max

        return vector_mutant

    def incrucisare(self, parinte, vector_mutant):
        vector_copil = np.copy(parinte)

        index_obligatoriu = random.randint(0, self.dim - 1)

        for j in range(self.dim):
            numar_aleator = random.random()  # Intre 0 si 1

            if numar_aleator < self.CR:
                vector_copil[j] = vector_mutant[j]
            elif j == index_obligatoriu:
                vector_copil[j] = vector_mutant[j]
            else:
                pass

        return vector_copil

    def selectie(self, index_parinte, vector_copil):
        scor_copil = self.fitness_func(vector_copil)
        scor_parinte = self.scoruri[index_parinte]

        if scor_copil < scor_parinte:
            return vector_copil, scor_copil
        else:
            return self.populatie[index_parinte], scor_parinte

    def optimizeaza(self):
        istoric = []

        idx_best = np.argmin(self.scoruri)
        best_sol = self.populatie[idx_best]
        best_score = self.scoruri[idx_best]
        istoric.append(best_score)

        for gen in range(self.max_gen):
            noua_populatie = np.copy(self.populatie)
            noi_scoruri = np.copy(self.scoruri)

            for i in range(self.pop_size):
                parinte = self.populatie[i]

                v_mutant = self.mutatie(i)

                v_copil = self.incrucisare(parinte, v_mutant)

                rez_vector, rez_scor = self.selectie(i, v_copil)

                noua_populatie[i] = rez_vector
                noi_scoruri[i] = rez_scor

                if rez_scor < best_score:
                    best_score = rez_scor
                    best_sol = rez_vector

            self.populatie = noua_populatie
            self.scoruri = noi_scoruri
            istoric.append(best_score)

        return best_sol, best_score, istoric