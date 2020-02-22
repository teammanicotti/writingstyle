import re
import string


class SentenceTools:
    @staticmethod
    def convert_pronoun(pronoun):
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
    def get_object_of_prep(parsed_sentence):
        for word in parsed_sentence:
            if "pobj" == word.dep_ and word.pos_ in ["PRON", "NOUN", "PROPN"] \
                    and word.head.dep_ == "agent":
                x = str(word.doc[word.left_edge.i: word.right_edge.i + 1])
                return x

    @staticmethod
    def get_verb_modifier(parsed_sentence):
        for word in parsed_sentence:
            if 'npadvmod' == word.dep_:
                return str(word.doc[word.left_edge.i: word.right_edge.i + 1])
        return ""

    @staticmethod
    def get_prepositions(parsed_sentence):
        prepositions = []
        for word in parsed_sentence:
            if word.dep_ == 'prep':
                prepositions.append(
                    str(word.doc[word.left_edge.i: word.right_edge.i + 1])
                )
        return prepositions

    @staticmethod
    def get_direct_object(parsed_sentence):
        direct_object = ""
        for word in parsed_sentence:
            if word.dep_ == 'dobj':
                direct_object = str(
                    word.doc[word.left_edge.i: word.right_edge.i + 1]
                )
        return direct_object

    @staticmethod
    def get_adverb(verb, parsed_sentence):
        adv = ""
        for word in parsed_sentence:
            if word.lemma_ == verb and word.doc[word.i - 1].dep_ == "advmod":
                adv = str(word.doc[word.i - 1].text)
        return adv

    @staticmethod
    def get_citation(parsed_sentence):
        left = 0
        right = 0
        if parsed_sentence[-1].text in ["]", ")"] or \
                parsed_sentence[-2].text in ["]", ")"]:
            for i in range(parsed_sentence[-1].i, 0, -1):
                if parsed_sentence[i].is_bracket and right == 0:
                    right = i
                elif parsed_sentence[i].is_bracket and right > 0:
                    left = i
                    break
            return str(parsed_sentence.doc[left: right + 1])
        return ""

    @staticmethod
    def get_subject(parsed_sentence):
        for word in parsed_sentence:
            if "subj" in word.dep_:
                x = str(
                    word.doc[
                        word.left_edge.i: word.right_edge.i + (
                            2 if word.doc[word.right_edge.i + 1].is_right_punct
                            else 1)
                        ]
                )
                return x

    @staticmethod
    def get_verb(parsed_sentence):
        verb = ""
        for word in parsed_sentence:
            if word.pos_ == "VERB":
                if word.dep_ == "ROOT":
                    verb = word.lemma_
                    break
                elif verb == "":
                    verb = word.lemma_
        return verb

    @staticmethod
    def build_sentence_from_list(parsed_sentence, components, punct):
        sentence = ' '.join(word for word in components)
        return SentenceTools.apply_capitalizations(parsed_sentence, sentence) \
               + punct

    @staticmethod
    def apply_capitalizations(parsed_sentence, recommendation):
        recommendation = recommendation.lower()
        phrases_to_be_capitalized = []
        compounds = []

        # Extract all substrings that need to be capitalized
        current_position = 0
        for i in range(len(parsed_sentence)):
            if i < current_position:
                continue

            if parsed_sentence[i].ent_type_ == "WORK_OF_ART":
                substring = ""
                while parsed_sentence[i].ent_type_ == "WORK_OF_ART":
                    substring += parsed_sentence[i].text
                    substring += (" " if parsed_sentence[i + 1].pos_
                                  not in ["PUNCT", "PART"] else "")
                    i += 1
                current_position = i
                phrases_to_be_capitalized.append(substring.strip())
            elif parsed_sentence[i].pos_ == "PROPN":
                phrases_to_be_capitalized.append(
                    str(parsed_sentence.doc[
                        parsed_sentence[i].left_edge.i: parsed_sentence[i].right_edge.i + 1]))
                if parsed_sentence[i].dep_ == "compound":
                    compounds.append(parsed_sentence[i].text)
                current_position = parsed_sentence[i].right_edge.i + 2

        # Swap all those substring with properly capitalized versions
        for phrase in phrases_to_be_capitalized:
            recommendation = re.sub(phrase.lower(), string.capwords(phrase),
                                    recommendation)

        # TODO: Why is this here? ~Devon
        # for phrase in compounds:
        #     recommendation = re.sub(phrase.lower(), phrase.upper(), recommendation, flags=re.I)
        return recommendation[0].upper() + recommendation[1:]
