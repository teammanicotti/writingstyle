"""
Passive to active: class containing method to identify passive voice
and generate new sentences in the active voice
Author: Robert Liedka (rl5849)
"""
import re
from seniorproject.recommendation.passivetoactive.SentenceTools import SentenceTools
from seniorproject.recommendation.recommendationengine import RecommendationEngine
from pattern.en import conjugate, PRESENT, PAST, PL, SG, INFINITIVE, PARTICIPLE #Yes, these always have red sqiggles under them
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.document import Document
from typing import List

class PassiveAnalyzer(RecommendationEngine):

    def __init__(self):
        super(PassiveAnalyzer, self).__init__()


    def analyze(self, doc: Document) -> List[Recommendation]:
        """
        Main analyze method
        :param doc:
        :return: Recommendation[]
        """
        results = []
        sentIndex = 0
        for paragraph in doc.paragraphs:
            for sent in paragraph.spacy_doc.sents:
                 results.extend(PassiveAnalyzer.AnnotateSentence(sent, sentIndex))
                 sentIndex += 1
        return results

    @staticmethod
    def AnnotateSentence(sentence, index):
        """
        Annotate sentence: Perform passive analysis and generate new sentence if passive
        :param sentence:
        :param index:
        :return: Recommendation[], empty array if not passive
        """
        results = []
        isPassive = False
        isHard = False
        reccomendPhrases = {}

        for word in sentence:
            if word.dep_ == "nsubjpass":
                isPassive = True
            elif word.dep_ == "auxpass":
                reccomendPhrases[word.text + " " + word.head.text] = {"index" : word.head.i }
                isPassive = True
            elif word.pos_ == "ADP" and word.right_edge.dep_ == "pobj":
                isHard = True

        if isPassive:
            for rec, info in reccomendPhrases.items():
                results.append(Recommendation(
                    RecommendationType.PASSIVE_TO_ACTIVE,
                    rec,
                    sentence.start,
                    sentence.end,
                    index, #sentence index
                    PassiveAnalyzer.CreateNewSentence(sentence),
                    0  # Confidence
                ))
        return results

    @staticmethod
    def CreateNewSentence(parsedSentence):
        """
        Create a new sentence: conjugate verb and re-order parts of speech to make an active
        voice sentence
        :param parsedSentence: spaCy object
        :return: array containing one sentence
        """
        #Questions never come out right
        if(parsedSentence[-1].text == "?"):
            return ""
        punct = "."
        if(parsedSentence[-1].is_punct):
            punct = parsedSentence[-1].text

        actor = SentenceTools.GetObjectOfPrep(parsedSentence)
        verb = SentenceTools.GetVerb(parsedSentence)
        subject = SentenceTools.GetSubject(parsedSentence)

        newSentece = []
        newActor = ""
        newVerb = ""
        adverb = SentenceTools.GetAdverb(verb, parsedSentence)
        citation = SentenceTools.GetCitation(parsedSentence)
        directObj = SentenceTools.GetDO(parsedSentence)

        if verb:
            try:
                newVerb = conjugate(verb=verb, tense=PAST, number=PL)
            except StopIteration:
                newVerb = verb
        if actor:
            newActor = SentenceTools.ConvertPronoun(actor)
        sentence = ""
        if(newActor and newVerb and subject):
            newSentece.append(newActor)
            if(adverb != ""):
                newSentece.append(adverb)
            newSentece.append(newVerb)
            newSentece.append(subject)
            if(directObj != ""):
                newSentece.append(directObj)
            modifier = SentenceTools.GetVerbModifier(parsedSentence)
            if(modifier != ""):
                newSentece.append(modifier)
            preps = SentenceTools.GetPrepositions(parsedSentence)
            if (len(preps) != 0):
                for prep in preps:
                    present = False
                    for component in newSentece:
                        if prep in component:
                            present = True
                    if not present:
                        newSentece.append(prep)
            if(citation != ""):
                newSentece.append(citation)

            if citation != "":
                for i in range(len(newSentece)):
                    if newSentece[i] != citation:
                        newSentece[i] = re.sub("\s*"+re.escape(citation), "", newSentece[i])

            sentence = SentenceTools.BuildSentenceFromList(parsedSentence, newSentece, punct)
        elif (newActor and newVerb):
            newSentece.append(newActor)
            newSentece.append(newVerb)
            sentence = "Consider rephrasing so that the actor is doing the activity... " + SentenceTools.BuildSentenceFromList(parsedSentence, newSentece, "...")
        elif (subject and newVerb):
            newSentece.append(subject)
            newSentece.append(newVerb)
            sentence = "Consider rephrasing so that the subject comes before the verb... " + SentenceTools.BuildSentenceFromList(parsedSentence, newSentece, "...")
        return [sentence]

    def __UseTestSet(self):
        with open("PassiveRecc.txt", "r") as ins:
            for line in ins:
                loadedSentence = self.nlp(line.strip())
                print(self.CreateNewSentence(loadedSentence))

if __name__ == '__main__':
    pa = PassiveAnalyzer()
    pa.UseTestSet()
    # while True:
    #     string = input("Sentence: ")
    #     change = []
    #     pa = PassiveAnalyzer()
    #     print(json.dumps(pa.AnnotateDoc(string.strip()), indent=4, sort_keys=True))






