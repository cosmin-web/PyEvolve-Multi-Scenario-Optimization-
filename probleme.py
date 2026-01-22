import numpy as np


# 1. CASA INTELIGENTA (Termodinamica + Baterie + Degradare + Dependente)
class ProblemaEnergie:
    def __init__(self):
        self.aparate = [
            (2.0, 2.1, "Masina Spalat", -1),
            (1.5, 2.5, "Uscator Rufe", 0),
            (4.0, 7.0, "Incarcare EV", -1),
            (1.0, 3.0, "Cuptor", -1),
            (1.5, 1.2, "Masina Vase", -1),
            (6.0, 0.4, "Ventilatie", -1),
            (24.0, 0.0, "Pompa Caldura", -1)
        ]

        #Temperatura exterioara
        self.temp_setata = 22.0
        self.temp_ext = np.array([-5, -6, -7, -6, -5, -3, 0, 2, 4, 6, 7, 8, 8, 7, 5, 3, 1, -1, -3, -4, -5, -6, -6, -5])

        # Solar
        self.solar = np.zeros(24)
        for h in range(24):
            if h >= 7 and h <= 17:
                # Formula Gaussiana
                numarator = -((h - 12) ** 2)
                numitor = 8.0
                self.solar[h] = 5.0 * np.exp(numarator / numitor)

        # Baterie si Retea
        self.cap_baterie = 13.5
        self.cost_ciclu_baterie = 0.5

        # Pret Retea
        self.pret_retea = []
        for h in range(24):
            if h >= 7 and h <= 23:
                self.pret_retea.append(0.65)
            else:
                self.pret_retea.append(0.30)

        self.limita_bransament = 9.0

    def get_limite(self):
        limite = []
        nr_aparate = len(self.aparate)

        for i in range(nr_aparate):
            if i == nr_aparate - 1:
                limite.append((0.5, 1.5))
            else:
                limite.append((0, 20))

        return limite

    def fitness(self, x):
        cost_bani = 0
        penalizare = 0
        consum_h = np.zeros(25)
        temp_casa = 20.0

        # Constrangere: Uscatorul trebuie dupa Masina
        start_masina = x[0]
        start_uscator = x[1]

        if start_uscator < start_masina + 2.0:
            penalizare += 5000

        for i in range(len(self.aparate) - 1):
            start = int(x[i])
            durata = self.aparate[i][0]
            putere = self.aparate[i][1]

            if start + durata > 24:
                penalizare += 500

            ora_final = min(start + int(durata) + 1, 24)
            for h in range(start, ora_final):
                consum_h[h] += putere

        # Simulare Termodinamica si Baterie
        baterie = 2.0
        factor_pompa = x[-1]

        for h in range(24):
            # A. COP Variabil in functie de temperatura de afara
            delta_t = self.temp_setata - self.temp_ext[h]

            # Eficienta scade cand e frig
            cop_calculat = 4.5 - (delta_t * 0.12)
            if cop_calculat < 1.5:
                cop_calculat = 1.5

            # B. Termodinamica
            pierdere_caldura = delta_t * 0.45
            caldura_generata = pierdere_caldura * factor_pompa
            consum_pompa = caldura_generata / cop_calculat

            temp_casa += caldura_generata - pierdere_caldura

            # C. Verificare siguranta
            total_consum = consum_h[h] + consum_pompa
            if total_consum > self.limita_bransament:
                diferenta = total_consum - self.limita_bransament
                penalizare += diferenta * 1000

            # D. Logica Baterie
            net = self.solar[h] - total_consum

            if net > 0:
                # Surplus -> incarcam bateria
                spatiu_liber = self.cap_baterie - baterie
                if net < spatiu_liber:
                    baterie += net
                else:
                    baterie += spatiu_liber
            else:
                # Deficit -> tragem din baterie sau retea
                necesar = abs(net)
                if baterie >= necesar:
                    baterie -= necesar
                    # Cost mic de uzura baterie
                    cost_bani += self.cost_ciclu_baterie * (necesar / self.cap_baterie)
                else:
                    tras_retea = necesar - baterie
                    baterie = 0
                    cost_bani += tras_retea * self.pret_retea[h]

            # E. Penalizare disconfort termic (deviatia de la 22 grade)
            deviatie = abs(self.temp_setata - temp_casa)
            cost_bani += deviatie * 15

        return cost_bani + penalizare


# 2. RUTA OPTIMA (Trafic Gaussian + Oboseala + Orar)
class ProblemaRuta:
    def __init__(self):
        self.nume = ["Acasa", "Client A", "Client B", "Depozit", "Vama", "Sediu", "Hotel"]
        self.n = len(self.nume)
        self.ferestre = [(0, 24), (9, 12), (13, 16), (7, 19), (0, 24), (8, 18), (14, 24)]
        self.durata_vizita = [0, 1.0, 1.5, 0.5, 1.0, 2.0, 0]

        np.random.seed(42)
        self.dist = np.random.rand(self.n, self.n) * 50
        np.fill_diagonal(self.dist, 0)

    def get_limite(self):
        limite = []
        for _ in range(self.n):
            limite.append((0, 1))
        return limite

    def get_trafic(self, ora):
        # Simulare trafic cu Gauss
        ora_mod = ora % 24

        exp_dimineata = -((ora_mod - 8.5) ** 2) / 1.5
        morning = 2.0 * np.exp(exp_dimineata)

        exp_seara = -((ora_mod - 17.5) ** 2) / 2.0
        evening = 2.5 * np.exp(exp_seara)

        return 1.0 + morning + evening

    def fitness(self, x):
        ordine = np.argsort(x)
        t_curent = 8.0
        t_condus_continuu = 0
        fitness_total = 0
        penalizare = 0

        for i in range(len(ordine) - 1):
            u = ordine[i]
            v = ordine[i + 1]
            dist_km = self.dist[u][v]

            trafic = self.get_trafic(t_curent)
            v_medie = 50.0 / trafic
            durata_ore = dist_km / v_medie

            factor_consum = 1 + (trafic - 1) * 0.6
            consum_l_100 = 7.0 * factor_consum
            litri = (dist_km / 100) * consum_l_100
            cost_benzina = litri * 7.5

            t_condus_continuu += durata_ore
            if t_condus_continuu > 4.0:
                t_curent += 0.75
                fitness_total += 0.75 * 50
                t_condus_continuu = 0

            t_curent += durata_ore
            fitness_total += (durata_ore * 60) + cost_benzina

            start_program = self.ferestre[v][0]
            end_program = self.ferestre[v][1]

            if t_curent < start_program:
                asteptare = start_program - t_curent
                t_curent += asteptare
                fitness_total += asteptare * 30
            elif t_curent > end_program:
                penalizare += 2000

            vizita = self.durata_vizita[v]
            t_curent += vizita

        return fitness_total + penalizare



# 3. PORTOFOLIU (Markowitz + Inflatie + Lichiditate)
class ProblemaPortofoliu:
    def __init__(self):
        self.active = [
            ("Tech Stocks", 0, 0),
            ("Real Estate", 0, 0),
            ("Gov Bonds", 0, 0),
            ("Crypto", 0, 0),
            ("Gold", 0, 0),
            ("Savings", 0, 0)
        ]
        self.rand = np.array([0.25, 0.12, 0.06, 0.80, 0.08, 0.03])
        self.risc_vol = np.array([0.30, 0.10, 0.02, 0.90, 0.15, 0.01])
        self.lichiditate = np.array([1.0, 0.2, 0.9, 1.0, 0.8, 1.0])
        self.n = len(self.active)

        # Matrice corelatie
        self.corr = np.array([
            [1.0, 0.2, -0.1, 0.7, -0.2, 0.0],
            [0.2, 1.0, -0.3, 0.1, 0.1, 0.0],
            [-0.1, -0.3, 1.0, -0.2, 0.4, 0.0],
            [0.7, 0.1, -0.2, 1.0, -0.1, 0.0],
            [-0.2, 0.1, 0.4, -0.1, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        ])

        # Calculam covarianta explicit
        self.cov = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                val = self.corr[i][j] * self.risc_vol[i] * self.risc_vol[j]
                self.cov[i][j] = val

        self.inflatie = 0.07  # 7% Inflatie
        self.pondere_risc = 3.0
        self.min_lichiditate = 0.6

    def get_limite(self):
        limite = []
        for _ in range(self.n):
            limite.append((0, 1))
        return limite

    def fitness(self, x):
        # Evitam impartirea la zero
        suma = np.sum(x)
        if suma < 1e-3:
            return 9999

        # Ponderi normalizate
        w = x / suma

        # 1. Randament Real
        rand_brut = np.dot(w, self.rand)
        cost_tranzactie = np.sum(w) * 0.015  # 1.5% comision
        rand_real = rand_brut - self.inflatie - cost_tranzactie

        # 2. Risc Portofoliu (Markowitz)
        # Varianta = w^T * Cov * w
        produs_inter = np.dot(self.cov, w)
        varianta_port = np.dot(w.T, produs_inter)
        risc_port = np.sqrt(varianta_port)

        # 3. Lichiditate
        scor_liq = np.dot(w, self.lichiditate)
        penalizare = 0
        if scor_liq < self.min_lichiditate:
            diferenta = self.min_lichiditate - scor_liq
            penalizare = diferenta * 50

        # Fitness = Risc - Randament (Minimizare)
        return (risc_port * self.pondere_risc) - rand_real + penalizare