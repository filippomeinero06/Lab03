from prestito import Prestito
from strumento import Strumento
from operator import attrgetter

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.__responsabile = responsabile
        self.__elenco_strumenti = [] # lista di oggetti di tipo Strumento
        self.__prestiti = [] # lista di oggetti di tipo Prestito

    @property
    def responsabile(self):
        return self.__responsabile

    @property
    def elenco_strumenti(self):
        return self.__elenco_strumenti

    @property
    def prestiti(self):
        return self.__prestiti

    @responsabile.setter
    def responsabile(self, responsabile):
        self.__responsabile = responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            infile = open(file_path, 'r')

            for line in infile:
                campi = line.strip().split(',')
                codice = campi[0]
                tipo = campi[1]
                marca = campi[2]
                anno = int(campi[3])
                prezzo = float(campi[4])

                s = Strumento(codice, tipo, marca, anno, prezzo) # creo l'oggetto di tipo Strumento
                self.elenco_strumenti.append(s)

            infile.close()
        except FileNotFoundError:
            raise



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""

        codici_s = []

        for s in self.elenco_strumenti:
            # s.codice[1:] -> prendo solo la parte numerica del codice (butto via la prima lettera "S")
            # int(s.codice[1:]) -> lo converto in intero
            # codici_s.append(int(s.codice[1:])) -> lo aggiungo alla lista di codici interi
            codici_s.append(int(s.codice[1:]))

        codici_s.sort() # ordino i codici (in ultmima posizione ci sarà il codice maggiore)
        max_cod = codici_s[-1]
        new_codice = "S" + str(max_cod+1) # mi creo il nuovo codice: incremento di 1 il codice max, lo converto in str e gli concateno davanti una "S"

        new_s = Strumento(new_codice, tipo, marca, anno_acquisto, valore) # creo il nuovo oggetto di tipo Strumento

        self.elenco_strumenti.append(new_s)

        return new_s


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.elenco_strumenti, key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # flag per controllare che lo strumento selezionato non sia già in prestito e che sia presente nell'elenco di strumenti
        gia_prestato = False
        strumento_presente = False

        if len(self.prestiti) > 0:
            for p in self.prestiti:
                if id_strumento == p.codice_strumento:
                    gia_prestato = True

        for s in self.elenco_strumenti:
            if id_strumento == s.codice:
                strumento_presente = True

        if gia_prestato:
            raise Exception(f"Errore: strumento {id_strumento} già prestato")
        elif not strumento_presente:
            raise Exception(f"Errore: strumento {id_strumento} non presente")
        else:
            cod_prestiti = []

            if len(self.prestiti) > 0:
                for p in self.prestiti:
                    cod_prestiti.append(int(p.codice_prestito[1:]))

                cod_prestiti.sort()
                max_cod = cod_prestiti[-1]
                new_codice = "P" + str(max_cod+1)
            else:
                new_codice = "P1"

            prestito = Prestito(new_codice, id_strumento, cognome_allievo, data)
            self.prestiti.append(prestito)

            return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""

        p_da_terminare = None
        for p in self.prestiti:
            if id_prestito == p.codice_prestito:
                p_da_terminare = p
                break

        if p_da_terminare is not None:
            self.prestiti.remove(p_da_terminare)
        else:
            raise Exception(f"Errore: prestito con codice {id_prestito} non presente")

