from json import load, dump
from tqdm.auto import tqdm
from itertools import combinations, product
from conceptnet_lite import Label, edges_between
import conceptnet_lite

from Tags import Tags
conceptnet_lite.connect(".\Database\conceptnet.db", db_download_url=None)


class Graph(Tags):
    def __init__(self, path='./Final_Model'):
        self.path = path
        super().__init__()
        white_tags = list(
            set(self.get_white_tags()) - set(self.get_black_tags()))
        # Initialise concepts
        self.concepts = {}
        for tag in tqdm(white_tags):
            self.add_concept(tag)

    def add_concept(self, tag):
        if tag not in self.concepts.keys():
            try:
                self.concepts[tag] = Label.get(text=tag.lower().replace(
                    '-', '_'), language='en').concepts
            except:
                # Black list tags that are not present in conceptnet

                self.remove(tag)

    def _fetch(self, word_1_concepts, word_2_concepts, word_1, word_2):
        edges = []
        relations_1 = []
        relations_2 = []
        for e in edges_between(word_1_concepts, word_2_concepts, two_way=False):
            relations_1.append(e.relation.name)
        for e in edges_between(word_2_concepts, word_1_concepts, two_way=False):
            relations_2.append(e.relation.name)

        if relations_1 == relations_2 and len(relations_1) != 0:
            edges.append((word_1, word_2, list(set(relations_1))))
            return edges
        if 'related_to' in relations_1 and 'related_to' in relations_2:
            relations_1.remove('related_to')
            relations_2.remove('related_to')
        if len(relations_1) != 0:
            edges.append((word_1, word_2, list(set(relations_1))))

        if len(relations_2) != 0:
            edges.append((word_2, word_1, list(set(relations_2))))
        return edges

    def generate_base_edge(self):
        white_tags = list(
            set(self.get_white_tags()) - set(self.get_black_tags()))
        for tag in tqdm(white_tags):
            self.add_concept(tag)
        edges = []
        white_tags = list(
            set(self.get_white_tags()) - set(self.get_black_tags()))
        pairs = list(combinations(white_tags, 2))
        for word_1, word_2 in tqdm(pairs):
            word_1_concepts = self.concepts[word_1]
            word_2_concepts = self.concepts[word_2]
            edges.extend(self._fetch(word_1_concepts,
                         word_2_concepts, word_1, word_2))
        with open('Data/Graph/base_edges.json', 'w') as f:
            dump(edges, f)

    def update(self):
        with open('Data/Graph/graphed_blue_tags.json') as f:
            graphed_blue_tags = load(f)
        to_graph_blues = [blue for blue in self.get_blue_tags(
        ) if blue not in graphed_blue_tags]
        white_tags = list(
            set(self.get_white_tags()) - set(self.get_black_tags()))
        all_tags = to_graph_blues + white_tags
        for tag in tqdm(all_tags):
            self.add_concept(tag)
        pairs = list(combinations(to_graph_blues, 2))
        pairs.extend(product(white_tags, to_graph_blues))
        edges = []
        for word_1, word_2 in tqdm(pairs):
            word_1_concepts = self.concepts[word_1]
            word_2_concepts = self.concepts[word_2]
            edges.extend(self._fetch(word_1_concepts,
                         word_2_concepts, word_1, word_2))
        with open('Data/Graph/extra_edges.json', 'w') as f:
            dump(edges, f)
        with open('Data/Graph/graphed_blue_tags.json', 'w') as f:
            dump(graphed_blue_tags + to_graph_blues, f)

    def get_edges(self):
        with open('Data/Graph/extra_edges.json') as f:
            ext_edges = load(f)
        with open('Data/Graph/base_edges.json') as f:
            base = load(f)
        all_edges = ext_edges + base
        edges = []
        for frm, to, rel in all_edges:
            edge = {}
            if 'antonym' not in rel:
                edge['source'] = frm
                edge['to'] = to
                edges.append(edge)
        return edges
