
import sys

class Gender:
    Male = 0
    Female = 1

class Graph(object):
    __slots__ = ['actresses', 'actors', 'n', 'm', 'role']
    def __init__(self) -> None:
        super().__init__()
        self.actresses = set()
        self.actors    = set()
        self.n         = 0
        self.m         = 0
        self.role      = None

    def parse_input(self) -> None:
        n, m = input().rstrip().split()
        self.n = int(n)
        self.m = int(m)

        self.actresses = {}
        for i in range(self.n):
            name = input().rstrip()
            self.actresses[name] = Actress(name, i)

        self.actors = {}
        for i in range(self.n):
            name = input().rstrip()
            self.actors[name] = Actor(name, i)

        people_dict = {**self.actresses, **self.actors}

        for _ in range(self.m):
            movie = Movie(input().rstrip())
            for _ in range(int(input().rstrip())):
                movie.add_cast(people_dict[input().rstrip()])
            for person in movie.female_cast:
                person.costarred |= movie.male_cast
            for person in movie.male_cast:
                person.costarred |= movie.female_cast
        
        self.role = input().rstrip()
        if self.role == "Veronique":
            self.play_veronique()
        else:
            self.play_mark()

    def play_veronique(self):
        actor_name = None
        while True:
            # Find out whether we are in a winning position
            winning = not self.match_all()

            actress = None
            if winning:
                # If we are in a winning situation, then
                # - if this is the first pick, 
                #   get list of unmatched actresses
                # - otherwise
                #   get list of unmatched actresses who are 
                #   adjacent to the previously picked actor
                if actor_name is None:
                    options = [actress for actress in self.actresses.values() if actress.match is None]
                else:
                    options = [actress for actress in set(self.actresses.values()) & self.actors[actor_name].costarred if actress.match is None]
                # Pick the first actress naively
                if options:
                    actress = options[0]
            else:
                # If we are not in a winning situation, then
                # - if this is the first pick,
                #   get list of all actresses
                # - otherwise
                #   get list of all actresses who are 
                #   adjacent to the previously picked actor.
                if actor_name is None:
                    options = list(self.actresses.values())
                else:
                    options = list(actress for actress in set(self.actresses.values()) & self.actors[actor_name].costarred)
                # Pick the first actress naively
                if options:
                    actress = options[0]
            
            # Reset actresses and actors for next iteration of checking whether
            # we are winning or not.
            self.reset()

            # If an actress is picked, remove it from being picked again
            # and output it
            # Otherwise output "IGiveUp"
            if actress:
                del self.actresses[actress.name]
                print(actress.name)
            else:
                print("IGiveUp")
            
            # Handle input
            actor_name = input().rstrip()
            actor = self.actors[actor_name]

            # Prevent this actor from being explored again
            actor.explored = self.n + 1

    def play_mark(self):
        while True:
            # Handle input
            actress_name = input().rstrip()
            actress = self.actresses[actress_name]

            # Find out whether we are in a winning position
            winning = self.match_all()

            # Remove the actress from being used again
            del self.actresses[actress_name]
            
            actor = None
            if winning:
                # If we are in a winning situation, 
                # pick the match of the aforementioned actress.
                actor = actress.match
            else:
                # If we are not in a winning situation, 
                # just naively pick an unpicked, adjacent actor.
                options = [actor for actor in actress.costarred if actor.explored < self.n]
                if options:
                    actor = options[0]
            
            # Reset actresses and actors for next iteration of checking whether
            # we are winning or not.
            self.reset()

            # If an actor is picked, remove it from being picked again
            # and output it
            # Otherwise output "IGiveUp"
            if actor:
                actor.explored = self.n + 1
                print(actor.name)
            else:
                print("IGiveUp")

    def reset(self):
        # Reset everything for next call 
        # of self.match_all()
        for actor in self.actors.values():
            if actor.explored < self.n:
                actor.explored = -1
            actor.match = None

        for actress in self.actresses.values():
            actress.match = None

    def match(self, actress, i):
        for func in (lambda act: not act.match, lambda act: act.match):
            for actor in actress.costarred:
                if func(actor) and actor.explored < i:
                    actor.explored = i
                    if actor.match is None or self.match(actor.match, i):
                        actor.match = actress
                        actress.match = actor
                        return True
        return False

    def match_all(self):
        pbm = True
        for i, actress in enumerate(sorted(self.actresses.values(), key=lambda a: len(a.costarred))):
            if not self.match(actress, i):
                pbm = False
        return pbm

class Movie(object):
    __slots__ = ['name', 'male_cast', 'female_cast']

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.male_cast = set()
        self.female_cast = set()
    
    def add_cast(self, person: "Person") -> None:
        if person.gender:
            self.female_cast.add(person)
        else:
            self.male_cast.add(person)
    
class Person(object):
    __slots__ = ['name', 'id', 'gender', 'match', 'costarred']
    
    def __init__(self, name: str, _id: int, gender: "Gender"):
        super().__init__()
        self.name      = name
        self.id        = _id
        self.gender    = gender
        self.match     = None
        self.costarred = set()

    def __hash__(self) -> int:
        return self.id

class Actress(Person):
    __slots__ = []

    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Female)

class Actor(Person):
    __slots__ = ['explored']
    
    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Male)
        self.explored = -1

if __name__ == "__main__":
    g = Graph()
    g.parse_input()