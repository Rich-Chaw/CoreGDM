from pathlib import Path
from typing import Union


def nx_to_graphtool(nx_graph, directed=False):
    """
    Read an edge list from a txt file using networkx and convert it to a graph-tool graph.
    Args:
        nx_graph: a networkx graph
        directed: Whether the graph is directed
    Returns:
        gt_graph: A graph-tool graph object
    """
    import networkx as nx
    import graph_tool as gt
    # Convert to graph-tool
    g = gt.Graph(directed=directed)
    node_map = {}
    for node in nx_graph.nodes():
        v = g.add_vertex()
        node_map[node] = v
    for u, v in nx_graph.edges():
        g.add_edge(node_map[u], node_map[v])
    return g


def load_graph(
    file: Union[Path, str],
    fmt="auto",
    ignore_vp=None,
    ignore_ep=None,
    ignore_gp=None,
    directed=False,
    **kwargs
):
    import warnings
    from graph_tool import load_graph_from_csv

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        from graph_tool import load_graph

    if (
        fmt == "auto"
        and isinstance(file, str)
        and Path(file).suffix[1:] in ["csv", "edgelist", "edge", "edges", "el", "txt"]
    ):
        delimiter = kwargs.get("delimiter", None)
        if delimiter is None:
            delimiter = "," if Path(file).suffix == ".csv" else " "
        if Path(file).suffix == ".csv":
            g = load_graph_from_csv(
                file,
                directed=directed,
                eprop_types=kwargs.get("eprop_types", None),
                eprop_names=kwargs.get("eprop_names", None),
                # string_vals=kwargs.get("string_vals", False),
                hashed=kwargs.get("hashed", False),
                hash_type=kwargs.get("hash_type", "string"),
                skip_first=kwargs.get("skip_first", False),
                ecols=kwargs.get("ecols", (0, 1)),
                csv_options=kwargs.get(
                    "csv_options", {"delimiter": delimiter, "quotechar": '"'}
                ),
            )
        elif Path(file).suffix == ".txt":
            import networkx as nx
            # the rest of this project expects undirected graphs 
            nx_graph = nx.read_edgelist(
                file,
                nodetype=int,
                create_using=nx.DiGraph() if directed else nx.Graph(),
                data=False
            )
            g = nx_to_graphtool(nx_graph, directed=False)
    else:
        g = load_graph(
            file,
            fmt=fmt,
            ignore_vp=ignore_vp,
            ignore_ep=ignore_ep,
            ignore_gp=ignore_gp,
            **kwargs
        )

    return g
