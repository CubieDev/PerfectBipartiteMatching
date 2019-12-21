
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
    def __init__(self) -> None:
        super().__init__()
        self.actresses = set()
        self.actors    = set()

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
        actress_dict = {}
        for i in range(self.n):
            name = data.pop(0)
            actress_dict[name] = Actress(name, i)

        # Construct a dict of Actors
        actor_dict = {}
        for i in range(self.n):
            name = data.pop(0)
            actor_dict[name] = Actor(name, i)

        # For convenience, get a dict consisting of all people
        people_dict = {**actress_dict, **actor_dict}

        # Get all movies. For each person starring in the movie,
        # update the person's costarred set with members they starred
        # with in this movie, of the opposite gender.
        for _ in range(self.m):
            movie = Movie(data.pop(0))
            for _ in range(int(data.pop(0))):
                movie.add_cast(people_dict[data.pop(0)])
            for person in movie.female_cast:
                person.costarred |= movie.male_cast
            for person in movie.male_cast:
                person.costarred |= movie.female_cast

        # Convert the dict to a set, leaving only the Actress
        # and Actor class instances
        self.actresses = {*actress_dict.values()}
        self.actors    = {*actor_dict.values()}
        
    def pick_winner(self):
        """
        Return Mark as the winner if all actresses can be matched
        with an actor. Return Veronique otherwise.
        """
        return "Mark" if self.match_all() else "Veronique"

    def match(self, actress):
        """
        Attempt to match actress with an actor.
        """
        # Iterate over all costarring actors twice. On the first iteration,
        # consider only actors without a match. On the second iteration,
        # consider only actors with a match.
        for func in (lambda act: not act.match, lambda act: act.match):
            for actor in actress.costarred:
                # Only consider actors that haven't been explored yet, for this actress.
                if func(actor) and not actor.explored:
                    # Set this actor to be explored for potential recursive cases
                    actor.explored = True
                    # If the actor is available, or if the actress currently matched
                    # with this actor can match with someone else, then we update the match
                    # and return True, indicating that the match was successful
                    if actor.match is None or self.match(actor.match): 
                        actor.match = actress
                        return True
        # If no possible match was found, return False
        return False

    def match_all(self):
        """
        Try to match all actresses with an actor. 
        If this fails for any actress, return False indicating
        that not all actresses could be matched.
        Otherwise return True
        """
        for actress in self.actresses:
            # Set explored to False for all actors. 
            # This allows `self.match` to avoid unwanted recursion.
            for a in self.actors:
                a.explored = False
            if not self.match(actress):
                return False
        return True

class Movie(object):
    """
    Movie stores a male and female cast, 
    as well as a name for this movie.
    """
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name        = name
        self.male_cast   = set()
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
    
    def __repr__(self) -> str:
        return f"<|{self.name}, starring: {', '.join(map(str, {**self.male_cast, **self.female_cast}))}|>"

class Person(object):
    """
    Person stores a name, id and gender for a person.
    It also stores a costarred set, which is a set of 
    Persons of the opposite gender that played in movies
    with this person.
    There is also a match variable which stores to which
    person this person is matched in a bipartite matching.
    """
    def __init__(self, name: str, _id: int, gender: "Gender"):
        super().__init__()
        self.name      = name
        self.id        = _id
        self.gender    = gender
        self.costarred = set()
        self.match     = None
    
    def __hash__(self) -> int:
        """
        Override default hashing function using 
        id for better performance
        """
        return self.id
    
    def __repr__(self) -> str: 
        return f"<{self.name}, {self.gender}>"

class Actress(Person):
    """
    Subclasses Person with default gender Female
    """
    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Female)

class Actor(Person):
    """
    Subclasses Person with default gender Male
    Also has explored variable used by Graph
    """
    def __init__(self, name: str, _id: int) -> None:
        super().__init__(name, _id, Gender.Male)
        self.explored = False

if __name__ == "__main__":
    g = Graph()
    g.parse_input()
    print(g.pick_winner())