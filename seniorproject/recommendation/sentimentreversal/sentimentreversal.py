"""
Sentiment reversal recommendation generator
Author: Robert Liedka (rl5849)
"""
from seniorproject.recommendation.recommendationengine import RecommendationEngine
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.document import Document
from nltk.corpus import wordnet
from typing import List

class SentimentReversal(RecommendationEngine):

    def __init__(self):
        super(SentimentReversal, self).__init__()

    def analyze(self, doc: Document) -> List[Recommendation]:
        """
        Main analyze method - Reports all recommendations for sentiment reversal
        Ex: He was not happy -> He was unhappy
        :param doc: Document
        :return: List of recommendations
        """
        results = []
        sentIndex = 0
        for paragraph in doc.paragraphs:
            for sent in paragraph.spacy_doc.sents:
                results.extend(SentimentReversal.GetAntonymsForSentence(sent, sentIndex))
                sentIndex += 1
        return results


    @staticmethod
    def GetAntonymsForSentence(sentence, sentenceIndex):
        """
        Generate recommendations for a sentence
        :param sentence: a spaCy sentence object
        :param sentenceIndex: Sentences index in doc
        :return: Recommendation[]
        """
        results = []

        for word in sentence:
            if word.text == 'not':
                ants = SentimentReversal.GetAntonymsForWord(sentence[word.i - sentence[0].i + 1].text)
                if(len(ants) > 0):
                    recText = ""
                    old_val = word.text + " " + sentence[word.i - sentence[0].i + 1].text
                    if len(ants) == 1:
                        recText = "Consider changing '{}' to {}.".format(old_val, ants[0])
                    elif len(ants) == 2:
                        recText = "Consider changing '{}' to {} or {}".format(old_val, ants[0], ants[1])
                    elif len(ants) > 2:
                        recText = "Consider changing '{}' to {}, {} or {}".format(old_val, ants[0], ants[1], ants[2])

                    results.append(Recommendation(
                        RecommendationType.SENTIMENT_REVERSAL,
                        "not " + sentence[word.i - sentence[0].i + 1].text,
                        word.i,  # word start index
                        word.i + 1,  # edge end index
                        sentenceIndex,  # sentence index
                        [recText],
                        0  # Confidence
                    ))
        return results
    
    
    @staticmethod
    def GetAntonymsForWord(word):
        """
        Get the antonyms for a specific word
        :param word: string
        :return: string[]
        """
        antonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
        return antonyms


    def __test(self):
        with open("testset.txt", "r") as ins:
            for line in ins:
                ants = self.GetAntonymsForSentence(line.strip())
                print(ants)



if __name__ == '__main__':
    AaaS = SentimentReversal()
    #sys.stdout = open('results.txt', 'w')
    AaaS.test()
    # while True:
    #     sentence = input("Word: ")
    #     print(AaaS.GetAntonymsForSentence(sentence))
