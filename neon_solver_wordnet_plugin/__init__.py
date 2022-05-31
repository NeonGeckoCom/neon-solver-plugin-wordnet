# # NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# # All trademark and other rights reserved by their respective owners
# # Copyright 2008-2021 Neongecko.com Inc.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import random

import nltk
import simplematch
from nltk.corpus import wordnet as wn

from neon_solvers import AbstractSolver


class WordnetSolver(AbstractSolver):
    def __init__(self):
        super(WordnetSolver, self).__init__(name="Wordnet")

    def extract_keyword(self, query, lang="en"):
        query = query.lower()

        # regex from narrow to broader matches
        match = None
        if lang == "en":
            match = simplematch.match("who is {query}", query) or \
                    simplematch.match("what is {query}", query) or \
                    simplematch.match("when is {query}", query) or \
                    simplematch.match("tell me about {query}", query)
        # TODO localization
        if match:
            match = match["query"]
        else:
            return None

        return match

    def get_data_key(self, query, lang="en"):
        # TODO localization
        if lang == "en":
            match = simplematch.match("what is {query} antonym*", query) or \
                    simplematch.match("what * antonym* {query}", query)
            if match:
                return "antonyms", match["query"]
            match = simplematch.match("what is {query} synonym*", query) or \
                    simplematch.match("what * synonym* {query}", query)
            if match:
                return "lemmas", match["query"]
            match = simplematch.match("what * definition* {query}", query) or \
                    simplematch.match("what * meaning* {query}", query) or \
                    simplematch.match("what is {query} definition", query) or \
                    simplematch.match("what is {query} meaning", query) or \
                    simplematch.match("what is {query}", query)
            if match:
                return "definition", match["query"]
        return None, query

    # officially exported Solver methods
    def get_data(self, query, context=None):
        pos = wn.NOUN  # TODO check context for postag
        synsets = wn.synsets(query, pos=pos)
        if not len(synsets):
            return {}
        synset = synsets[0]
        res = {"lemmas": Wordnet.get_lemmas(query, pos=pos, synset=synset),
               "antonyms": Wordnet.get_antonyms(query, pos=pos, synset=synset),
               "holonyms": Wordnet.get_holonyms(query, pos=pos, synset=synset),
               "hyponyms": Wordnet.get_hyponyms(query, pos=pos, synset=synset),
               "hypernyms": Wordnet.get_hypernyms(query, pos=pos, synset=synset),
               "root_hypernyms": Wordnet.get_root_hypernyms(query, pos=pos, synset=synset),
               "definition": Wordnet.get_definition(query, pos=pos, synset=synset)}
        return res

    def get_spoken_answer(self, query, context=None):
        lang = context.get("lang") or self.default_lang
        lang = lang.split("-")[0]
        # extract the best keyword with some regexes or fallback to RAKE
        k, query = self.get_data_key(query, lang)
        if not query:
            query = self.extract_keyword(query, lang) or query
        data = self.search(query, context)
        if k and k in data:
            v = data[k]
            if k in ["lemmas", "antonyms"] and len(v):
                return random.choice(v)
            if isinstance(v, list) and len(v):
                v = v[0]
            if isinstance(v, str):
                return v
        # definition
        return data.get("definition")


class Wordnet:
    nltk.download("wordnet")
    nltk.download('omw-1.4')

    @staticmethod
    def get_synsets(word, pos=wn.NOUN):
        synsets = wn.synsets(word, pos=pos)
        if not len(synsets):
            return []
        return synsets

    @staticmethod
    def get_definition(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        return synset.definition()

    @staticmethod
    def get_examples(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        return synset.examples()

    @staticmethod
    def get_lemmas(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        return [l.name().replace("_", " ") for l in synset.lemmas()]

    @staticmethod
    def get_hypernyms(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        return [l.name().split(".")[0].replace("_", " ") for l in
                synset.hypernyms()]

    @staticmethod
    def get_hyponyms(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        return [l.name().split(".")[0].replace("_", " ") for l in
                synset.hyponyms()]

    @staticmethod
    def get_holonyms(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        return [l.name().split(".")[0].replace("_", " ") for l in
                synset.member_holonyms()]

    @staticmethod
    def get_root_hypernyms(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        return [l.name().split(".")[0].replace("_", " ") for l in
                synset.root_hypernyms()]

    @staticmethod
    def common_hypernyms(word, word2, pos=wn.NOUN):
        synsets = wn.synsets(word, pos=pos)
        if not len(synsets):
            return []
        synset = synsets[0]
        synsets = wn.synsets(word2, pos=pos)
        if not len(synsets):
            return []
        synset2 = synsets[0]
        return [l.name().split(".")[0].replace("_", " ") for l in
                synset.lowest_common_hypernyms(synset2)]

    @staticmethod
    def get_antonyms(word, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(word, pos=pos)
            if not len(synsets):
                return []
            synset = synsets[0]
        lemmas = synset.lemmas()
        if not len(lemmas):
            return []
        lemma = lemmas[0]
        antonyms = lemma.antonyms()
        return [l.name().split(".")[0].replace("_", " ") for l in antonyms]

    @classmethod
    def query(cls, query, pos=wn.NOUN, synset=None):
        if synset is None:
            synsets = wn.synsets(query, pos=pos)
            if not len(synsets):
                return {}
            synset = synsets[0]
        res = {"lemmas": cls.get_lemmas(query, pos=pos, synset=synset),
               "antonyms": cls.get_antonyms(query, pos=pos, synset=synset),
               "holonyms": cls.get_holonyms(query, pos=pos, synset=synset),
               "hyponyms": cls.get_hyponyms(query, pos=pos, synset=synset),
               "hypernyms": cls.get_hypernyms(query, pos=pos, synset=synset),
               "root_hypernyms": cls.get_root_hypernyms(query, pos=pos, synset=synset),
               "definition": cls.get_definition(query, pos=pos, synset=synset)}
        return res

