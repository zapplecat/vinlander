import networkx
import os
import spacy

# TOOD: Swap this out for larger model
nlp = spacy.load("en_core_web_md")


def write_graph_to_pickle(graph, filename, nlp_attrib='nlp_vector'):
    # Accept a filter func
    for node in graph.nodes:
        if graph.nodes[node]['soc_type'] == 'detailed':
            graph.nodes[node][nlp_attrib] = nlp(
                graph.nodes[node]['job_description'])
    pickle_filepath = os.path.join(
        os.path.abspath('./data'), filename)
    networkx.write_gpickle(graph, pickle_filepath)


def get_node_similarity(
        node1, node2, comparison_attrib='job_description'):
    """Gets the description similarilty between leaf nodes.
    """
    doc1 = nlp(node1[comparison_attrib])
    doc2 = nlp(node2[comparison_attrib])
    return doc1.similarity(doc2)


def get_node_similarity_from_graph(
        graph, node1, node2, nlp_attrib='nlp_vector'):
    if not graph.has_node(node1):
        raise RuntimeError("node1 {} is not in graph".format(node1))
    elif not graph.has_node(node2):
        raise RuntimeError("node2 {} is not in graph".format(node2))
    return graph.nodes[node1][nlp_attrib].similarity(
        graph.nodes[node2][nlp_attrib])
