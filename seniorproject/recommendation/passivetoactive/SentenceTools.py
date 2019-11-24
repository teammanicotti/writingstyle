import re
import string
class SentenceTools():
    @staticmethod
    def ConvertPronoun(pronoun):
        if pronoun == "me":
            return "i"
        elif pronoun == "him":
            return "he"
        elif pronoun == "her":
            return "she"
        elif pronoun == "them":
            return "they"
        else:
            return pronoun

    @staticmethod
    def GetObjectOfPrep(parsedSentence):
        for word in parsedSentence:
            if "pobj" == word.dep_ and word.pos_ in ["PRON", "NOUN", "PROPN"] and word.head.dep_ == "agent":
                x = str(word.doc[word.left_edge.i: word.right_edge.i + 1])
                return x

    @staticmethod
    def GetVerbModifier(parsedSentence):
        for word in parsedSentence:
            if 'npadvmod' == word.dep_:
                return str(word.doc[word.left_edge.i: word.right_edge.i + 1])
        return ""

    @staticmethod
    def GetPrepositions(parsedSentence):
        prepositions = []
        for word in parsedSentence:
            if word.dep_ == 'prep':
                prepositions.append(str(word.doc[word.left_edge.i: word.right_edge.i + 1]))
        return prepositions

    @staticmethod
    def GetDO(parsedSentence):
        directObject = ""
        for word in parsedSentence:
            if word.dep_ == 'dobj':
                directObject = str(word.doc[word.left_edge.i: word.right_edge.i + 1])
        return directObject

    @staticmethod
    def GetAdverb(verb, parsedSentence):
        adv = ""
        for word in parsedSentence:
            if word.lemma_ == verb and word.doc[word.i - 1].dep_ == "advmod":
                adv = str(word.doc[word.i - 1].text)
        return adv

    @staticmethod
    def GetCitation(parsedSentence):
        left = 0
        right = 0
        if parsedSentence[-1].text in ["]", ")"] or parsedSentence[-2].text in ["]", ")"]:
            for i in range(parsedSentence[-1].i, 0, -1):
                if(parsedSentence[i].is_bracket and right == 0):
                    right = i
                elif(parsedSentence[i].is_bracket and right > 0):
                    left = i
                    break
            return str(parsedSentence.doc[left : right + 1])
        return ""

    @staticmethod
    def GetSubject(parsedSentence):
        for word in parsedSentence:
            if "subj" in word.dep_:
                x = str(word.doc[word.left_edge.i : word.right_edge.i + (2 if word.doc[word.right_edge.i+1].is_right_punct else 1)])
                return x

    @staticmethod
    def GetVerb(parsedSentence):
        verb = ""
        for word in parsedSentence:
            if word.pos_ == "VERB":
                if word.dep_ == "ROOT":
                    verb = word.lemma_
                    break
                elif verb == "":
                    verb = word.lemma_
        return verb


    @staticmethod
    def BuildSentenceFromList(parsedSentence, components, punct):
        sentence = ' '.join(word for word in components)
        return SentenceTools.ApplyCapitalizations(parsedSentence, sentence) + punct

    @staticmethod
    def ApplyCapitalizations(parsedSentence, recommendation):
        recommendation = recommendation.lower()
        phrasesToBeCapitalized = []
        compounds = []

        #Extract all substrings that need to be capitalized
        currentPosition = 0
        for i in range(len(parsedSentence)):
            if i < currentPosition:
                continue

            if parsedSentence[i].ent_type_ == "WORK_OF_ART":
                substring = ""
                while parsedSentence[i].ent_type_ == "WORK_OF_ART":
                    substring += parsedSentence[i].text
                    substring += (" " if parsedSentence[i+1].pos_ not in ["PUNCT", "PART"] else "")
                    i += 1
                currentPosition = i
                phrasesToBeCapitalized.append(substring.strip())
            elif parsedSentence[i].pos_ == "PROPN":
                phrasesToBeCapitalized.append(
                    str(parsedSentence.doc[parsedSentence[i].left_edge.i: parsedSentence[i].right_edge.i + 1]))
                if parsedSentence[i].dep_ == "compound":
                        compounds.append(parsedSentence[i].text)
                currentPosition = parsedSentence[i].right_edge.i + 2

        #Swap all those substring with properly capitalized versions
        for phrase in phrasesToBeCapitalized:
            recommendation = re.sub(phrase.lower(), string.capwords(phrase), recommendation)
        # for phrase in compounds:
        #     recommendation = re.sub(phrase.lower(), phrase.upper(), recommendation, flags=re.I)
        return recommendation[0].upper() + recommendation[1:]