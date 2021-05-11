# Perfect Bipartite Matching

This repository holds a solution to a problem, which can be reconstructed as a perfect bipartite matching problem, which I was tasked to solve. Two versions of the code are provided - one with comments, and one without. The remainer of this README is an explanation of the Problem. The paper regarding the problem, algorithm, results, complexities and proofs is also provided as [paper.pdf](paper.pdf).

---

## Problem
We were tasked to find out which player has the winning strategy in the following game:

>Veronique and Mark play the following game:  Veronique starts by naming an actress u, then Mark responds with an actor v which has co-starred with u, then Veronique names an actress w which co-stars with actor v, and so on.  Of course they are not allowed to name the same actress or actor twice. The first player who gets stuck (i.e. is not able to respond any more) loses.
>
>Given a fixed set of actresses X, a fixed set of actors Y and a fixed list of movies with casts, this is a finite game where both players have all information. So either Veronique or Mark should have a winning strategy (i.e. able to always win, no matter what moves the other player makes).
>
>Veronique always starts.

---

## Input
Input to the program is given via **stdin**, in the following format:
```
2 2
DianaKruger
MelanieLaurent
BradPitt
NormanReedus
IngloriousBasterds
3
DianaKruger
MelanieLaurent
BradPitt
Sky
2
DianaKruger
NormanReedus
```

The first line contains integers *n* with *1 <= n* and *m* with *0 <= m*, which represent the number of actors/actresses and the amount of movies respectively. Note that *|X| = |Y| = n*.
Following this line is *n* lines of names of actresses, and then *n* lines of names of actors.
Then *m* times the following:
* The name of the movie.
* The cast size *s* with *1 <= s <= 1000* of the movie, as an integer.
* *s* lines of cast members.
All names are unique.

---

## Output
Output should be given via **stdout**. The program should either output `Mark` or `Veronique`, depending on who has the winning strategy.

---

### Contributing
I am not taking contributions for this repository, as it is designed as an archive.

---

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.
