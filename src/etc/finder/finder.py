import pandas
import logging

class Finder:
    def __init__(self, dictionnary, sounds):
        self.regex_patern = ""
        self.sounds = sounds
        self.data = pandas.read_csv(dictionnary, header=None, names=['alphabet', 'phonetic'])

    def generate_patern(self, number):
        
        exclude_syllables = '|'.join(sum(self.sounds, []))
        excluse_pattern = f"[^{exclude_syllables}|,]*"

        if (number == ''):
            self.regex_patern = f"/{excluse_pattern}/"
        else:
            syllables = []
            for num in number :
                logging.info(f"num = {num}, symbol = {self.sounds[int(num)]}")
                syllables.append(self.sounds[int(num)])

            logging.info(f"syllables = {syllables}")

            self.regex_patern = "/"
            for symbol in syllables :
                self.regex_patern += f"{excluse_pattern}({'|'.join(symbol)})"

            self.regex_patern += f"{excluse_pattern}/"

        logging.info(f"regex patern = {self.regex_patern}")

    def get_matches(self, number):
        self.generate_patern(number)
        filtered_data = self.data[self.data["phonetic"].str.contains(self.regex_patern, regex=True) == True]
        return filtered_data