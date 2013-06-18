import argparse

class LMArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='A lazy SPARQL dataset linker',
                                              epilog='Happy linking!')
        self.parser.add_argument('-t', 
                                 '--threshold', 
                                 nargs=1, 
                                 dest='t',
                                 type=self.restricted_float,
                                 default=[0.9], 
                                 help='Levenshtein ratio threshold (0.9 if not specified)')
        self.parser.add_argument('-e',
                                 '--endpoint',
                                 nargs=1,
                                 dest='e',
                                 required=True,
                                 help='URL address of the SPARQL endpoint to query')
        self.parser.add_argument('-g1',
                                 '--named-graph1',
                                 nargs=1,
                                 dest='g1',
                                 required=True,
                                 help='URI of the first named graph to link')
        self.parser.add_argument('-g2',
                                 '--named-graph2',
                                 nargs=1,
                                 dest='g2',
                                 required=True,
                                 help='URI of the second named graph to link')
        self.parser.add_argument('-p1',
                                 '--property1',
                                 nargs=1,
                                 dest='p1',
                                 required=True,
                                 help='URI of the first property to link')
        self.parser.add_argument('-p2',
                                 '--property2',
                                 nargs=1,
                                 dest='p2',
                                 required=True,
                                 help='URI of the second property to link')
        self.parser.add_argument('-v',
                                 '--verbose',
                                 action='store_const',
                                 const=1,
                                 dest='v',
                                 help='Be verbose')
        self.args = self.parser.parse_args()
    def restricted_float(self,x):
        x = float(x)
        if x < 0.0 or x > 1.0:
            raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
        return x
