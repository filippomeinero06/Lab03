class Prestito:
    def __init__(self, codice_prestito, codice_strumento, cognome_allievo, data):
        self.__codice_prestito = codice_prestito
        self.__codice_strumento = codice_strumento
        self.__cognome_allievo = cognome_allievo
        self.__data = data

    @property
    def codice_prestito(self):
        return self.__codice_prestito

    def __str__(self):
        return f"{self.__codice_prestito} {self.__codice_strumento} {self.__cognome_allievo} {self.__data}"
