
import sys

class Gender:
    Male = 0
    Female = 1

class Graph(object):
    def __init__(self) -> None:
        super().__init__()
        self.actresses = None
        self.actors    = None
        self.movies    = None

    def parse_input(self) -> None:
        data = sys.stdin.read().splitlines()
        n, m = data.pop(0).split()
        self.n = int(n)
        self.m = int(m)

        actress_dict = {}
        for i in range(self.n):
            name = data.pop(0)
            actress_dict[name] = Actress(name, i)

        actor_dict = {}
        for i in range(self.n):
            name = data.pop(0)
            actor_dict[name] = Actor(name, i)

        people_dict = {**actress_dict, **actor_dict}

        for _ in range(self.m):
            #name = data.pop(0)
            movie = Movie(data.pop(0))
            for _ in range(int(data.pop(0))):
                #person = people_dict[data.pop(0)]
                movie.add_cast(people_dict[data.pop(0)])
                #person.starred_in(movie)
            for person in movie.female_cast:
                person.costarred |= movie.male_cast
            for person in movie.male_cast:
                person.costarred |= movie.female_cast
            #for person in movie.cast:
            #    person.costarred |= {a for a in movie.cast if a.gender != person.gender}

        self.actresses = {*actress_dict.values()}
        self.actors    = {*actor_dict.values()}

        #self.people_dict = people_dict

        #for key in people_dict:
        #    people_dict[key].prepare()
        
    def pick_winner(self):
        return "Mark" if self.match_all() else "Veronique"

    def match(self, actress):
        for func in (lambda act: not act.match, lambda act: act.match):
            for actor in actress.costarred:
                if func(actor) and not actor.explored:
                    actor.explored = True
                    if actor.match is None or self.match(actor.match): 
                        actor.match = actress
                        actress.match = actor
                        return True
        return False

    def match_all(self): 
        for actress in self.actresses:
            for a in self.actors:
                a.explored = False
            if not self.match(actress):
                return False
        return True

    def plot(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        g = nx.DiGraph()
        values = [v for v in self.people_dict.values() if v.costarred]
        g.add_nodes_from([v.name for v in values])
        color = []
        for vertex in values:
            g.add_edges_from([(vertex.name, edge.name) for edge in vertex.costarred if vertex.match != edge])
            color += ["gray"] * len(vertex.costarred)
            if vertex.match:
                g.add_edge(vertex.name, vertex.match.name)
                color[-1] = "red"
        nx.draw(g, 
                with_labels=True, 
                node_color=['y' if vertex.gender == "M" else 'g' for vertex in values], 
                edge_color=color,
                pos = nx.drawing.layout.bipartite_layout(g, [v.name for v in values if v.gender == "M"]))
        plt.draw()
        plt.show()

class Movie(object):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.male_cast = set()
        self.female_cast = set()
    
    def add_cast(self, person: "Person") -> None:
        if person.gender == Gender.Male:
            self.male_cast.add(person)
        else:
            self.female_cast.add(person)
    
    #def get_cast(self, gender: "Gender") -> "Set(Person)":
    #    if gender == Gender.Male:
    #        return self.female_cast
    #    return self.male_cast

    def __repr__(self) -> str:
        return f"<|{self.name}, starring: {', '.join(map(str, self.cast))}|>"

class Person(object):
    def __init__(self, name: str, _id: int, gender: "Gender"):
        super().__init__()
        self.name             = name
        self.id               = _id
        self.gender           = gender
    #    self.starred          = set()
        self.costarred        = set()
        self.match = None
    
    #def prepare(self) -> None:
    #    self.costarred = set().union(*(movie.get_cast(self.gender) for movie in self.starred))
    
    #def starred_in(self, movie: "Movie") -> None:
    #    self.starred.add(movie)

    def __hash__(self) -> int:
        return self.id
    
    def __repr__(self) -> str: 
        return f"<{self.name}, {self.gender}>"

class Actress(Person):
    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Female)

class Actor(Person):
    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Male)
        self.explored = False

if __name__ == "__main__":
    #from time import time
    #t = time()
    g = Graph()
    g.parse_input()
    #print(f"\n{time() - t:8f}s input parsing")
    #t = time()
    print(g.pick_winner())
    #print(f"{time() - t:8f}s algorithm time")