
import sys

class Gender:
    """
    Simple class to use as enum for differentiating Actors and Actresses. 
    Normally I'd import Enum from enum, 
    but the import takes time unnecessarily.
    """
    Male = 0
    Female = 1

class Graph(object):
    """
    Graph stores two sets of Persons, one for Actresses
    and one for Actors. These sets get filled by parse_input,
    which reads an input. A winner between Mark and Veronique
    is calculated within this class, by attempting to match
    all actors and actresses.
    """
    __slots__ = ['actresses', 'actors', 'n', 'm', 'full']
    def __init__(self) -> None:
        super().__init__()
        self.actresses = set()
        self.actors    = set()
        self.n         = 0
        self.m         = 0
        self.full      = True

    def parse_input(self) -> None:
        """
        Parsing input data and storing the values in the Actress
        and Actor sets.
        """
        # Read all data, and split by lines
        data = sys.stdin.read().splitlines()
        # Get the n and m from the data
        n, m = data.pop(0).split()
        self.n = int(n)
        self.m = int(m)

        # Construct a dict of Actresses
        self.actresses = {}
        for i in range(self.n):
            name = data.pop(0)
            self.actresses[name] = Actress(name, i)

        # Construct a dict of Actors
        self.actors = {}
        for i in range(self.n):
            name = data.pop(0)
            self.actors[name] = Actor(name, i)

        # For convenience, get a dict consisting of all people
        people_dict = {**self.actresses, **self.actors}

        # Convert the dict to a set, leaving only the Actress
        # and Actor class instances
        self.actresses = {*self.actresses.values()}
        self.actors    = {*self.actors.values()}

        # For all movies, update the set of costars of all 
        # actresses. Also shrink the actor set.
        for _ in range(self.m):
            movie = Movie(data.pop(0))
            for _ in range(int(data.pop(0))):
                movie.add_cast(people_dict[data.pop(0)])
            for person in movie.female_cast:
                person.costarred |= movie.male_cast
            self.actors -= movie.male_cast
        
        # If the actor set is not empty, then there is an actor
        # who was not in any movie. 
        if self.actors:
            self.full = False
    
    def pick_winner(self) -> str:
        """
        Return Mark as the winner if all actresses can be matched
        with an actor. Return Veronique otherwise.
        """
        return "Mark" if self.match_all() else "Veronique"

    def match(self, actress: "Actress", i: int) -> bool:
        """
        Attempt to match actress with an actor.
        i is used to ensure that no infinite recursion occurs.
        """
        # Iterate over all costarring actors twice. On the first iteration,
        # consider only actors without a match. On the second iteration,
        # consider only actors with a match.
        for func in (lambda act: not act.match, lambda act: act.match):
            for actor in actress.costarred:
                # Only consider actors that haven't been explored yet, for this i.
                if func(actor) and actor.explored != i:
                    # Set this actor to be explored for potential recursive cases
                    actor.explored = i
                    # If the actor is available, or if the actress currently matched
                    # with this actor can match with someone else, then we update the match
                    # and return True, indicating that the match was successful
                    if actor.match is None or self.match(actor.match, i):
                        actor.match = actress
                        return True
        # If no possible match was found, return False
        return False

    def match_all(self) -> bool:
        """
        Try to match all actresses with an actor. 
        If this fails for any actress, return False indicating
        that not all actresses could be matched.
        Otherwise return True
        """
        # If there are actors who haven't played in any movie, return False,
        # as this actor can not be matched.
        if not self.full:
            return False

        # Iterate over sorted actresses
        for i, actress in enumerate(sorted(self.actresses, key=lambda a: len(a.costarred))):
            # Attempt to match the actress. Pass index i to ensure no infinite recursion
            if not self.match(actress, i):
                return False
        return True

class Movie(object):
    """
    Movie stores a male and female cast, 
    as well as a name for this movie.
    """
    __slots__ = ['name', 'male_cast', 'female_cast']
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.male_cast = set()
        self.female_cast = set()
    
    def add_cast(self, person: "Person") -> None:
        """
        Add this person either to the male or
        female cast.
        """
        if person.gender == Gender.Male:
            self.male_cast.add(person)
        else:
            self.female_cast.add(person)
    
class Person(object):
    """
    Person stores a name, id and gender for a person.
    """
    __slots__ = ['name', 'id', 'gender']
    def __init__(self, name: str, _id: int, gender: "Gender"):
        super().__init__()
        self.name      = name
        self.id        = _id
        self.gender    = gender

    def __eq__(self, other):
        """
        Override default equals function using 
        id for better performance with set unions
        """
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Override default hashing function using 
        id for better performance when hashing for sets
        """
        return self.id

class Actress(Person):
    """
    Subclass of Person
    Actress stores a costarred set, which is a set of 
    Actors that played in movies with this actress.
    """
    __slots__ = ['costarred']

    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Female)
        self.costarred = set()

class Actor(Person):
    """
    Subclass of Person
    Actor has a match variable which stores to which
    actress this actor is matched in a bipartite matching.
    It also stores an explored variable to prevent 
    infinite recursion in Graph().match()
    """
    __slots__ = ['explored', 'match']
    
    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Male)
        self.explored = -1
        self.match     = None

if __name__ == "__main__":
    g = Graph()
    g.parse_input()
    print(g.pick_winner())