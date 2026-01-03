# Analiza regulilor de asociere pe date FAO GIFT

Acest repository conține codul sursă utilizat pentru preprocesarea datelor
și identificarea itemset-urilor frecvente folosind algoritmii FP-Growth
și Apriori, aplicate pe seturi de date FAO privind consumul alimentar individual.
## Date
Seturile de date utilizate provin din platforma FAO GIFT:
https://www.fao.org/gift-individual-food-consumption/data/en

## Observații
Codul a fost rulat în Google Colab. Pentru stabilitatea execuției au fost utilizate
praguri de suport diferite pentru FP-Growth și Apriori, precum și un eșantion
de tranzacții, în funcție de limitările hardware.
