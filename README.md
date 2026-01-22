# Optimizare Evolutivă (Differential Evolution)

Acest proiect implementează un algoritm de **Evoluție Diferențială (DE)** pentru rezolvarea unor probleme complexe de optimizare din lumea reală. Aplicația include un motor de calcul bazat pe populații de soluții și o interfață grafică (GUI) pentru monitorizarea procesului de învățare în timp real.

---

### Tehnologii Utilizate
* **Python 3.x** - Limbajul de bază.
* **NumPy** - Procesare vectorială pentru manipularea eficientă a populației.
* **Matplotlib** - Vizualizarea grafică a curbei de convergență.
* **Tkinter** - Interfață grafică pentru utilizator.

---

### 1. Algoritmul de Evoluție Diferențială
Algoritmul optimizează o funcție obiectiv prin îmbunătățirea iterativă a unei populații de vectori. Etapele implementate sunt:

* **Inițializare**: Generarea aleatorie a populației în spațiul căutării.
* **Mutație**: Crearea unui vector mutant folosind formula:  
  $V = a + F \cdot (b - c)$
* **Încrucișare**: Amestecarea genelor vectorului mutant cu cele ale părintelui curent pe baza probabilității $CR$.
* **Selecție**: Alegerea supraviețuitorului pentru generația următoare pe baza scorului de fitness (doar dacă descendentul este mai bun decât părintele).

---

### 2. Probleme de Optimizare Implementate

#### **A. Consum Energie (Smart Home)**
* **Costuri**: Minimizează factura electrică utilizând prețuri dinamice.
* **Energie Verde**: Maximizează autoconsumul din panouri solare și gestionarea bateriei.
* **Termodinamică**: Respectă constrângeri de confort interior vs. pierderi de căldură.
<img width="954" height="717" alt="image" src="https://github.com/user-attachments/assets/96db3e41-ff8c-41dd-8ea3-063f86c2064d" />


#### **B. Rută Optimă**
* **Trafic**: Calculează traseul minim luând în calcul traficul variabil (ore de vârf).
* **Program**: Respectă ferestrele de livrare impuse de clienți.
* **Resurse**: Include penalizări pentru oboseala șoferului și consumul de carburant.
<img width="954" height="717" alt="image" src="https://github.com/user-attachments/assets/4e59728a-408e-4f90-92a9-1ff1bf748a85" />


#### **C. Portofoliu Investiții**
* **Markowitz**: Utilizează modelul de risc prin matricea de Covarianță.
* **Echilibru**: Balansează randamentul așteptat cu volatilitatea (riscul).
* **Factori Externi**: Include inflația, lichiditatea și costurile de tranzacție.
<img width="954" height="717" alt="image" src="https://github.com/user-attachments/assets/3879e2ab-1e3e-410c-a279-b7e500668c9d" />

---

### Structura Codului
* `algoritm.py` - Conține logica matematică a Evoluției Diferențiale.
* `probleme.py` - Conține definițiile funcțiilor de fitness și constrângerile specifice.
* `interfata.py` - Codul pentru interfața grafică și vizualizarea datelor.

---

### Parametrii Algoritmului (Recomandați)

| Parametru | Descriere | Interval Recomandat |
| :--- | :--- | :--- |
| **Mărime Populație** | Numărul de soluții candidate evaluate simultan. | 20 - 50 |
| **Număr Generații** | Numărul de iterații ale procesului evolutiv. | 100 - 1000 |
| **Factor Mutație (F)** | Controlează amplificarea diferenței dintre vectori. | 0.5 - 0.8 |
| **Probabilitate CR** | Șansa ca un parametru să fie moștenit de la mutant. | 0.6 - 0.9 |

---

### Instalare și Utilizare

1. **Clonarea depozitului:**
   ```bash
   git clone [https://github.com/utilizator/proiect-ia-evolutiv.git](https://github.com/utilizator/proiect-ia-evolutiv.git)
   cd proiect-ia-evolutiv

2. **Instalarea bibliotecilor necesare:**
   ```pip instal numpy matplotlib```

3. **Rularea aplicatiei:**
   ```python3 interfata.py```
