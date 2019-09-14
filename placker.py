#!/usr/bin/env python3
import itertools
import json
import os
import string


class Placker:
    def __init__(self, input_text, master_text, check_synonyms=True, min_len=3, save=False):
        self.save = save
        self.mutator_list = []
        self.master_list = []
        self.masterdict = {}
        self.inputdict = {}
        self.input_text = input_text
        self.master_text = master_text
        self.input_text = self.input_text.replace("- ", "")
        self.master_text = self.master_text.replace("- ", "")
        self.check_synonyms = check_synonyms
        self.min_len = min_len
        if check_synonyms:
            self.synonyms = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/support/src.json', 'r'))
        self.preprocess()
        # self.find_plagiarism()

    def preprocess(self):
        preprocessor = str.maketrans(string.ascii_uppercase, string.ascii_lowercase, string.punctuation)
        self.unprocessed_input_list = self.input_text.translate(str.maketrans("", "", string.punctuation)).split()
        self.input_list = self.input_text.translate(preprocessor).split()
        self.word_plags = [0]*len(self.unprocessed_input_list)
        self.mlist = self.master_text.translate(preprocessor).split()
        for k in range(len(self.mlist) - self.min_len + 1):
            self.masterdict[tuple(self.mlist[k:self.min_len + k])] = 1

    def find_synonym(self,i):
        self.mutator_list = []
        for pos, word in enumerate(self.check_str):
            if word in list(self.synonyms.keys()):
                temp_syns = []
                for key, value in list(self.synonyms[word].items()):
                    temp_syns += value
                self.mutator_list.append(list(set(temp_syns)))
            else:
                self.mutator_list.append([word])

        # iterate all possible combos           
        self.master_list = list(itertools.product(*self.mutator_list))

        for some_list in self.master_list:
            # check for plagiarism
            if self.masterdict.get(tuple(some_list), None):
                for index in range(i, self.min_len + i):
                    self.word_plags[index] = 1

    def find_plagiarism(self):
        for i, j in enumerate(self.input_list):
            self.master_list = []
            self.check_str = self.input_list[i:self.min_len + i]
            if len(self.check_str) < self.min_len:
                continue
            if self.check_str not in self.master_list:
                self.master_list.append(self.check_str)

            if self.check_synonyms is True:
                self.find_synonym(i)
            else:
                if self.masterdict.get(tuple(self.check_str), None):
                    for index in range(i, self.min_len + i):
                        self.word_plags[index] = 1

        for i, word_plag in enumerate(self.word_plags):
            if word_plag == 1:
                self.unprocessed_input_list[i] = "<span style=\"color:red\">{}</span>".format(self.unprocessed_input_list[i])

        plag_text = " ".join(self.unprocessed_input_list)
        if self.save:
            with open("out.md", "w") as f:
                f.write(plag_text)
        else:
            return plag_text

if __name__ == "__main__":
    save = False
    # quick = Placker(open(sys.argv[1], 'r').read(), open(sys.argv[2], 'r').read(), sys.argv[3], int(sys.argv[4]))
    quick = Placker("Quickly check and visualise plagiarism between two documents.", "Quickly stop and visualise plagiarism between two documents.", True, 3)
    print(quick.find_plagiarism())
