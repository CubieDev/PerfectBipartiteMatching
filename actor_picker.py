
from time import time
import sys

# TODO: Use an enum everywhere
class Player:
    V = 0
    M = 1

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

        # TODO: Consider storing ID to has on, rather than hashing on name

        actress_dict = {}
        for _ in range(self.n):
            name = data.pop(0)
            actress_dict[name] = Actress(name)
        
        actor_dict = {}
        for _ in range(self.n):
            name = data.pop(0)
            actor_dict[name] = Actor(name)

        people_dict = {**actress_dict, **actor_dict}

        movie_dict = {}
        for _ in range(self.m):
            name = data.pop(0)
            s = int(data.pop(0))
            movie = Movie(name, s)
            for _ in range(s):
                person = people_dict[data.pop(0)]
                movie.add_cast(person)
                person.starred_in(movie)
            movie_dict[name] = movie

        self.actresses = {*actress_dict.values()}
        self.actors    = {*actor_dict.values()}
        self.movies    = {*movie_dict.values()}

        for key in people_dict:
            people_dict[key].prepare()
            #print(key, "has costarred with", people_dict[key].costarred)

    def pick_winner(self):
        return "Mark" if self._pick_winner((self.actresses, self.actors), Actress(""), 0) else "Veronique"

    def _pick_winner(self, people: "Tuple(Set(Actress), Set(Actor))", prev_picked: "Person", turn: int) -> int:
        # TODO: Change turn and return to some enum

        #print(turn, ["V", "M"][turn % 2])

        # Turn % 2 = 0: Veronique's turn
        # Turn % 2 = 1: Mark's turn

        #print(people)
        #options = people[turn % 2]
        #if turn > 0:
        #    print(prev_picked.costarred)
        #    print(people[turn % 2] & prev_picked.costarred)
        #    options &= prev_picked.costarred

        #print(options)
        for option in (people[turn % 2] & prev_picked.costarred if turn > 0 else people[turn % 2]):
            #print(" " * turn, ["V", "M"][turn % 2], "tries", option)
            # TODO: Change to have less set operations
            #       Perhaps add `option` to `option.costarred_...`
            # If the current player always wins by choosing `option`, then return
            if self._pick_winner((people[0] - {option}, people[1] - {option}),
                                 option,
                                 turn + 1) == turn % 2:
                return turn % 2
            
        # If options is empty, or the winner regardless of our choice is the opponent, 
        # we return the opponents' id.
        return (turn + 1) % 2
    
class Movie(object):
    def __init__(self, name: str, cast_size: int) -> None:
        super().__init__()
        self.name = name
        self.cast = set()
        self.cast_size = cast_size
    
    def add_cast(self, person: "Person") -> None:
        self.cast.add(person)
    
    def __repr__(self) -> str:
        return f"<|{self.name}, starring: {', '.join(map(str, self.cast))}|>"

class Person(object):
    def __init__(self, name: str, gender: str):
        super().__init__()
        self.name             = name
        self.gender           = gender # "M" or "F"
        self.starred          = set()
        # TODO: Consider one set for costarred
        #self.costarred_female = set()
        #self.costarred_male   = set()
        self.costarred        = set()
    
    def prepare(self) -> None:
        self.costarred = set().union(*(movie.cast for movie in self.starred))
    
    def starred_in(self, movie: "Movie") -> None:
        self.starred.add(movie)
        
        # TODO: Make this more efficient:
        #for person in movie.cast:
        #    if person.gender == "F":
        #        self.costarred_female.add(person)
        #    else:
        #        self.costarred_male.add(person)
        #self.costarred |= movie.cast

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __repr__(self) -> str: 
        return f"<{self.name}, {self.gender}>"

class Actress(Person):
    def __init__(self, name: str):
        super().__init__(name, "F")

class Actor(Person):
    def __init__(self, name: str):
        super().__init__(name, "M")

if __name__ == "__main__":
    g = Graph()
    g.parse_input()
    print(g.pick_winner())
    