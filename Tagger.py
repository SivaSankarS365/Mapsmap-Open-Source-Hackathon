from load_model import make_model
from Tags import Tags
from Tags import Tags

from sense2vec import Sense2VecComponent
from sklearn.feature_extraction.text import CountVectorizer
import spacy

from itertools import product
nlp = spacy.load("en_core_web_md")
s2v = nlp.add_pipe("sense2vec")
s2v.from_disk(r'Data\Embeddings\s2v_old')


class Tagger(Tags):
    """Main class for providing tag recommendations"""

    def __init__(self, base_path=r'Data'):
        super().__init__(base_path)
        self.mlb_keys, self.AI_model = make_model()

    def decode(self, y, cutoff):
        scores = dict(zip(self.mlb_keys, y))
        cur_pred = {}
        for key, score in scores.items():
            if score > cutoff:
                cur_pred[key] = score
        tags = sorted(list(cur_pred.keys()), key=lambda x: -cur_pred[x])
        probs = [cur_pred[tag] for tag in tags]
        return list(zip(tags, probs))

    def AI_predict(self, text, cutoff=0.7, return_scores=False):
        p = self.AI_model.predict([text])
        y = self.decode(p[0], cutoff)
        if return_scores:
            return y
        else:
            ret = [tag for tag, _ in y]
            return ret

    def get_nouns(self, text):
        n_gram_range = (1, 2)
        stop_words = "english"
        try:
            count = CountVectorizer(ngram_range=n_gram_range,
                                    stop_words=stop_words).fit([text])
        except:
            return None
        all_candidates = count.get_feature_names_out()
        doc = nlp(text)
        noun_phrases = set(chunk.text.strip().lower()
                           for chunk in doc.noun_chunks)
        nouns = set()
        for token in doc:
            if token.pos_ == "NOUN" and token.is_stop == False:
                nouns.add(token.text)
        all_nouns = nouns.union(noun_phrases)
        all_nouns = list(
            set([noun.replace(' ', '_').replace('-', '_').lower() for noun in all_nouns]))
        all_nouns = [
            noun for noun in all_nouns if noun in self.available_words]
        candidates = list(
            filter(lambda candidate: candidate in all_nouns, all_candidates))
        return candidates

    def blues_predict(self, text, cutoff=0.7):
        preds = []
        nouns = self.get_nouns(text)
        if nouns is None:
            return []
        blues = self.get_blue_tags()
        for x, y in product(blues, nouns):
            score = []
            try:  # If failed use spacy itself
                score.append(nlp(x)[0]._.s2v_similarity(nlp(y)[0]))
            except:
                x = x.replace('_', ' ')
                y = y.replace('_', ' ')
                score.append(nlp(x)[0].similarity(nlp(y)[0]))
            if score[0] > cutoff:
                preds.append(x)
        return list(set(preds))

    def predict(self, text, blues_cutoff=0.7, AI_cutoff=0.7):
        base_preds = set(self.AI_predict(text, cutoff=AI_cutoff))
        blues_preds = set(self.blues_predict(text, cutoff=blues_cutoff))
        preds = base_preds.union(blues_preds) - set(self.get_black_tags())
        return list(preds)
