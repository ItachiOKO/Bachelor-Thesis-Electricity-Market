1. Allgemeine Konventionen

snake_case für alle nicht-konstanten Python-Variablen und Funktionen

UPPER_SNAKE_CASE für Konstanten und Config-Entries (z. B. in config.py)

PascalCase für Klassennamen


2. Pyomo-Modellkomponenten

v_ + UPPER_SNAKE_CASE > Entscheidungsvariablen

p_ + UPPER_SNAKE_CASE -> Parameter 

c_ + UPPER_SNAKE_CASE -> Constraints

e_ + UPPER_SNAKE_CASE -> Expressions 


3. Marktarten

| Kürzel | Bedeutung               |
| ------ | ----------------------- |
| ID     | Intraday                |
| DA     | Day-Ahead               |
| AUC    | Auktion                 |
| CONT   | Kontinuierlich          |


4. Regelleistung

| Kürzel | Bedeutung             |
| ------ | --------------------- |
| PRL    | Primärregelleistung   |
| SRL    | Sekundärregelleistung |


5. Handelsgrößen


| Kürzel    | Bedeutung       |
| --------- | --------------- |
| BUY_VOL  | Kaufvolumen     |
| SELL_VOL | Verkaufsvolumen |

6. Weiteres

| Kürzel    | Bedeutung       |
| --------- | --------------- |
| BAT       | Battery         |
|  |  |

