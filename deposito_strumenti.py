from prestito import Prestito
from strumento import Strumento
from operator import attrgetter

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.__responsabile = responsabile
        self.__elenco_strumenti = [] # lista che conterrà gli oggetti di tipo Strumento
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

                s = Strumento(codice, tipo, marca, anno, prezzo)
                self.elenco_strumenti.append(s)

            infile.close()
        except FileNotFoundError:
            raise



    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""

        codici_s = []

        for s in self.elenco_strumenti:
            codici_s.append(int(s.codice[1:]))

        codici_s.sort()
        max_cod = codici_s[-1]
        new_codice = "S" + str(max_cod+1)

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
                if id_strumento == p.codice_prestito:
                    gia_prestato = True

        for s in self.elenco_strumenti:
            if id_strumento == s.codice:
                strumento_presente = True

        if gia_prestato or not strumento_presente:
            print(f"Errore: strumento {id_strumento} già prestato o non presente")
            raise Exception # TODO sistemare il messaggio di eccezione che riceve il main()
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

        p_trovato = False
        for p in self.prestiti:
            if id_prestito == p.codice_prestito:
                p_da_terminare = p
                p_trovato = True
                break

        if p_trovato:
            self.prestiti.remove(p_da_terminare)
        else:
            print(f"Errore: il prestito con codice {id_prestito} non presente")
            raise Exception
