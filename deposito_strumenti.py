import csv
from operator import attrgetter
from prestito import Prestito
from strumento import Strumento


class DepositoStrumenti:

    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        self.strumenti.clear()
        try:
            with open(file_path, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for riga in reader:
                    codice, tipo, marca, anno_acquisto, valore = riga
                    s = Strumento(
                        codice, tipo, marca, int(anno_acquisto), float(valore)
                    )
                    self.strumenti.append(s)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} non trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        if self.strumenti:
            ultimi_codici = [int(s.codice[1:]) for s in self.strumenti]
            nuovo_id = max(ultimi_codici) + 1
        else:
            nuovo_id = 1
        codice = f"S{nuovo_id}"

        s = Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(s)
        return s

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        # Utilizza attrgetter come mostrato nelle soluzioni di riferimento
        return sorted(self.strumenti, key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        strumento = None
        for s in self.strumenti:
            if s.codice == id_strumento:
                strumento = s
                break

        if strumento is None:
            raise Exception(f"Strumento {id_strumento} non trovato.")
        if not strumento.disponibile:
            raise Exception(f"Lo strumento {id_strumento} è già in prestito.")

        prestito = Prestito(data, id_strumento, cognome_allievo)
        strumento.disponibile = False
        self.prestiti.append(prestito)
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        prestito = None
        for p in self.prestiti:
            if p.codice == id_prestito:
                prestito = p
                break

        if prestito is None:
            raise Exception(f"Prestito {id_prestito} non trovato.")

        # Rende nuovamente disponibile lo strumento
        for s in self.strumenti:
            if s.codice == prestito.id_strumento:
                s.disponibile = True
                break

        # Rimuove il prestito dal sistema
        self.prestiti.remove(prestito)
