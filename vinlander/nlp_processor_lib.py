import networkx
import os
import spacy

nlp = spacy.load("en_core_web_md")

def write_graph_to_pickle(graph):
    for node in graph.nodes:
        if node in code_map['detailed']:
            graph.nodes[node]['nlp_vector'] = nlp(
                graph.nodes[node]['job_description'])
    pickle_filepath = os.path.join(
        os.path.abspath('./data'), 'nlp_md_graph')
    networkx.write_gpickle(graph, pickle_filepath)
