class Strumento:
    def __init__(self, codice, tipo, marca, anno, prezzo):
        self.__codice = codice
        self.__tipo = tipo
        self.__marca = marca
        self.__anno = anno
        self.__prezzo = prezzo

    def __str__(self):
        return f"{self.__codice} {self.__tipo} {self.__marca} {self.__anno} {self.__prezzo}"

    @property
    def codice(self):
        return self.__codice

    @property
    def marca(self):
        return self.__marca

