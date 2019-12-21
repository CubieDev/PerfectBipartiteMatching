
import sys

class Gender:
    Male = 0
    Female = 1

class Graph(object):
    def __init__(self) -> None:
        super().__init__()
        self.actresses = set()
        self.actors    = set()

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
            movie = Movie(data.pop(0))
            for _ in range(int(data.pop(0))):
                movie.add_cast(people_dict[data.pop(0)])
            for person in movie.female_cast:
                person.costarred |= movie.male_cast
            for person in movie.male_cast:
                person.costarred |= movie.female_cast

        self.actresses = {*actress_dict.values()}
        self.actors    = {*actor_dict.values()}
        
    def pick_winner(self):
        return "Mark" if self.match_all() else "Veronique"

    def match(self, actress):
        for func in (lambda act: not act.match, lambda act: act.match):
            for actor in actress.costarred:
                if func(actor) and not actor.explored:
                    actor.explored = True
                    if actor.match is None or self.match(actor.match): 
                        actor.match = actress
                        return True
        return False

    def match_all(self): 
        for actress in self.actresses:
            for a in self.actors:
                a.explored = False
            if not self.match(actress):
                return False
        return True

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
    
    def __repr__(self) -> str:
        return f"<|{self.name}, starring: {', '.join(map(str, self.cast))}|>"

class Person(object):
    def __init__(self, name: str, _id: int, gender: "Gender"):
        super().__init__()
        self.name      = name
        self.id        = _id
        self.gender    = gender
        self.costarred = set()
        self.match     = None
    
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
    g = Graph()
    g.parse_input()
    print(g.pick_winner())