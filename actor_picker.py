
import sys

class Gender:
    Male = 0
    Female = 1

class Graph(object):
    __slots__ = ['actresses', 'actors', 'n', 'm', 'full']
    def __init__(self) -> None:
        super().__init__()
        self.actresses = set()
        self.actors    = set()
        self.n         = 0
        self.m         = 0
        self.full      = True

    def parse_input(self) -> None:
        data = sys.stdin.read().splitlines()
        n, m = data.pop(0).split()
        self.n = int(n)
        self.m = int(m)

        self.actresses = {}
        for i in range(self.n):
            name = data.pop(0)
            self.actresses[name] = Actress(name, i)

        self.actors = {}
        for i in range(self.n):
            name = data.pop(0)
            self.actors[name] = Actor(name, i)

        people_dict = {**self.actresses, **self.actors}

        self.actresses = {*self.actresses.values()}
        self.actors    = {*self.actors.values()}

        for _ in range(self.m):
            movie = Movie(data.pop(0))
            for _ in range(int(data.pop(0))):
                movie.add_cast(people_dict[data.pop(0)])
            for person in movie.female_cast:
                person.costarred |= movie.male_cast
            self.actors -= movie.male_cast
        
        if self.actors:
            self.full = False
    
    def pick_winner(self):
        return "Mark" if self.match_all() else "Veronique"

    def match(self, actress, i):
        for func in (lambda act: not act.match, lambda act: act.match):
            for actor in actress.costarred:
                if func(actor) and actor.explored != i:
                    actor.explored = i
                    if actor.match is None or self.match(actor.match, i):
                        actor.match = actress
                        return True
        return False

    def match_all(self):
        if not self.full:
            return False

        for i, actress in enumerate(sorted(self.actresses, key=lambda a: len(a.costarred))):
            if not self.match(actress, i):
                return False
        return True

class Movie(object):
    __slots__ = ['name', 'male_cast', 'female_cast']

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
    
class Person(object):
    __slots__ = ['name', 'id', 'gender']
    def __init__(self, name: str, _id: int, gender: "Gender"):
        super().__init__()
        self.name      = name
        self.id        = _id
        self.gender    = gender

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self) -> int:
        return self.id

class Actress(Person):
    __slots__ = ['costarred']

    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Female)
        self.costarred = set()

class Actor(Person):
    __slots__ = ['explored', 'match']
    
    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Male)
        self.explored = -1
        self.match     = None

if __name__ == "__main__":
    g = Graph()
    g.parse_input()
    print(g.pick_winner())