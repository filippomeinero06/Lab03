from strumento import Strumento
from operator import attrgetter

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.__responsabile = responsabile
        self.elenco_strumenti = [] # lista che conterrà gli oggetti di tipo Strumento
        self.prestiti = [] # lista dei prestiti [codice_prestito, codice_strumento, cognome_allievo, data_prestito]

    @property
    def responsabile(self):
        return self.__responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self.__responsabile = responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        infile = None
        try:
            infile = open(file_path, 'r')

            for line in infile:
                campi = line.strip().split(',')
                codice = campi[0]
                tipo = campi[1]
                marca = campi[2]
                anno = int(campi[3])
                prezzo = float(campi[4])

                s = Strumento(codice, tipo, marca, anno, prezzo)
                self.elenco_strumenti.append(s)
        except FileNotFoundError:
            raise
        finally:
            if infile is not None:
                infile.close()



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""

        codici_s = []

        for s in self.elenco_strumenti:
            codici_s.append(s.codice)

        # es. "S8"
        cod_max = codici_s[-1] # prendo l'ultimo codice della lista (il maggiore)

        cod_max = cod_max[1:] # tolgo da cod_max la S iniziale e tengo solo il numero
        cod_max = int(cod_max) + 1 # incremento di 1 il codice massimo

        new_codice = "S" + str(cod_max)

        new_s = Strumento(new_codice, tipo, marca, anno_acquisto, valore)

        self.elenco_strumenti.append(new_s)

        return new_s


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        self.elenco_strumenti.sort(key=attrgetter('marca'))
        return self.elenco_strumenti

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        gia_prestato = False
        strumento_presente = False

        if len(self.prestiti) > 0:
            for p in self.prestiti:
                if id_strumento == p[1]:
                    gia_prestato = True

        for s in self.elenco_strumenti:
            if id_strumento == s.codice:
                strumento_presente = True

        if gia_prestato or not strumento_presente:
            raise Exception # TODO sistemare il messaggio di eccezione che riceve il main()
        else:
            cod_prestiti = []
            if len(self.prestiti) > 0:
                for p in self.prestiti:
                    cod_prestiti.append(p[0])

                cod_max = cod_prestiti[-1]
                cod_max = cod_max[1:]
                cod_max = int(cod_max) + 1
                new_codice = "P" + str(cod_max)
            else:
                new_codice = "P1"

            prestito = [new_codice, id_strumento, cognome_allievo, data]
            self.prestiti.append(prestito)

            return f"{prestito[0]}, {prestito[1]}, {prestito[2], prestito[3]}"

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # TODO
