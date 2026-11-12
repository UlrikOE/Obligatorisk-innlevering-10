import csv
import glob
from datetime import datetime
from matplotlib import pyplot as plt
from statistics import median

månedsdata = {}
maks_per_måned = {}
min_per_måned = {}
maks_snødybde_måned = {}
tot_nedbør_måned = {}
maks_midvind_måned = {}
stasjoner = {}

filer = glob.glob("Værdata/*.csv")


for fil in filer:
    with open(fil, "r", encoding="utf-8") as fila:
        leser = csv.reader(fila, delimiter=";")
        next(leser)

        for rad in leser:
            stasjonsnavn = rad[0]
            stasjonsnummer = rad[1].strip()

            if stasjonsnummer.startswith("SN"):
                stasjoner[stasjonsnummer] = stasjonsnavn


for stasjonsnummer in stasjoner:
    print(stasjonsnummer, stasjoner[stasjonsnummer])

while True:
    stasjon_valg = input("Skriv inn stasjonsnummer: ").strip()

    if stasjon_valg not in stasjoner:
        print("Ugyldig stasjonsnummer!")
    else:
        break

for fil in filer:
    with open(fil, "r", encoding="utf-8") as fila:
        leser = csv.reader(fila, delimiter=";")
        next(leser)

        for rad in leser:
            if rad[1].strip() != stasjon_valg:
                continue

            if rad[2].strip() == "":
                continue

            dato = datetime.strptime(rad[2], "%d.%m.%Y")

            år_måned = (dato.year, dato.month)

            if år_måned in månedsdata:
                månedsdata[år_måned].append(rad)
            else:
                månedsdata[år_måned] = [rad]

for år_måned in månedsdata:
    mid_temp = []
    snødybde = []
    nedbør = []
    høy_midvind = []

    for rad in månedsdata[år_måned]:

        if rad[4].strip() != "-" and rad[4].strip() != "":
            mid_temp.append(float(rad[4].strip().replace(",", ".")))

        if rad[7].strip() != "-" and rad[7].strip() != "":
            snødybde.append(float(rad[7].strip().replace(",", ".")))

        if rad[5].strip() != "-" and rad[5].strip() != "":
            nedbør.append(float(rad[5].strip().replace(",", ".")))

        if rad[6].strip() != "-" and rad[6].strip() != "":
            høy_midvind.append(float(rad[6].strip().replace(",", ".")))

    if høy_midvind:
        maks_midvind = max(høy_midvind)
        maks_midvind_måned[år_måned] = maks_midvind

    if len(nedbør) > 20:
        tot_nedbør = sum(nedbør)
        tot_nedbør_måned[år_måned] = tot_nedbør

    if snødybde:
        maks_snødybde = max(snødybde)
        maks_snødybde_måned[år_måned] = maks_snødybde

    if mid_temp:
        maks_måned = max(mid_temp)
        maks_per_måned[år_måned] = maks_måned
        min_måned = min(mid_temp)
        min_per_måned[år_måned] = min_måned


datoer = []
snødybder = []

for år_måned in sorted(maks_snødybde_måned):
    snødybder.append(maks_snødybde_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    datoer.append(dato)

nedbør_datoer = []
nedbør_verdier = []

for år_måned in sorted(tot_nedbør_måned):
    nedbør_verdier.append(tot_nedbør_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    nedbør_datoer.append(dato)

maks_temp_verdier = []
maks_temp_datoer = []

for år_måned in sorted(maks_per_måned):
    maks_temp_verdier.append(maks_per_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    maks_temp_datoer.append(dato)

min_temp_verdier = []
min_temp_datoer = []

for år_måned in sorted(min_per_måned):
    min_temp_verdier.append(min_per_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    min_temp_datoer.append(dato)

maks_midvind_verdier = []
maks_midvind_datoer = []

for år_måned in sorted(maks_midvind_måned):
    maks_midvind_verdier.append(maks_midvind_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    maks_midvind_datoer.append(dato)

fig, ax = plt.subplots(5, 1, figsize=(12, 10), sharex=True)

ax[0].plot(datoer, snødybder)
ax[1].plot(nedbør_datoer, nedbør_verdier)
ax[2].plot(maks_temp_datoer, maks_temp_verdier)
ax[3].plot(min_temp_datoer, min_temp_verdier)
ax[4].plot(maks_midvind_datoer, maks_midvind_verdier)

ax[0].set_ylabel("cm")
ax[1].set_ylabel("mm")
ax[2].set_ylabel("°C")
ax[3].set_ylabel("°C")
ax[4].set_ylabel("m/s")

ax[0].set_title("Maks Snødybde")
ax[1].set_title("Total Nedbør")
ax[2].set_title("Maks Temperatur")
ax[3].set_title("Min Temperatur")
ax[4].set_title("Maks Middelvind")

plt.tight_layout()

sommerdager = {}
høysommerdager = {}
tropedager = {}

for år_måned in månedsdata:

    år = år_måned[0]

    if år not in sommerdager:
        sommerdager[år] = 0
        høysommerdager[år] = 0
        tropedager[år] = 0

    for rad in månedsdata[år_måned]:

        if rad[3].strip() == "-" or rad[3].strip() == "":
            continue

        temperatur = float(rad[3].strip().replace(",", "."))

        if temperatur > 20:
            sommerdager[år] += 1

        if temperatur > 25:
            høysommerdager[år] += 1

        if temperatur > 30:
            tropedager[år] += 1

årstall = sorted(sommerdager)

fig2, ax2 = plt.subplots(figsize=(12, 6))

ax2.plot(årstall, [sommerdager[år] for år in årstall], label="Sommerdager")

ax2.plot(årstall, [høysommerdager[år] for år in årstall], label="Høysommerdager")

ax2.plot(årstall, [tropedager[år] for år in årstall], label="Tropedager")

ax2.set_xlabel("År")
ax2.set_ylabel("Antall dager")
ax2.set_title("Sommerdager, høysommerdager og tropedager")
ax2.legend()
ax2.grid(True)

fig2.tight_layout()
