# Weekly Report

May 3, 2019

Wei Lu

## Week: July 28th - Aug 1st

### Goals

- Find out why PAC without sampling and original top covering are producing different results
- Implement brute force search and split algorithm to discover stable parition
- More writing

### Activities

- Two algorithm outputs are different because PAC implementation is buggy - it shouldn't consider coalitions containing players that have already been removed. Fixed.
- Implemented a search and split algorithm to find stable partition
- Fixed core stability check - the ``better-off'' check was too weak, it completely ignored unknown coalition for a player, it should have checked through the complete preference list instead
- Make top responsive check more efficient by only checking known coalitions.
- Discovered that the derived Knesset game isn't top responsive. Removing the participation term from the value function didn't help.
- Read paper - Simple priorities and core stability in hedonic games: http://fmwww.bc.edu/repec/esNASM04/up.9919.1074605860.pdf
- Report: 1 page


### Meeting Agenda: Aug 2nd

- After fixes with restrictive loop still many singletons and slow. Since the 100-run results are already stable, can we ditch restrictive loop for good for our case?
- How to make Knesset game top responsive?
- Suspecion: top covering algorithm work on some non-top responsive games too?
- Discuss search split algo results
- Suspecion: search split algo may not always terminate
- Is it meaningful to find solution that maximizes social welfare in our case?


## Week: July 17th - July 28th

### Goals

- Get the latest data: redownload data in case data has been updated since last download
- Evaluate data quality: find out which endpoint provide more consistent data within itself
- Literature review: Coalition structure generation: A survey https://www.sciencedirect.com/science/article/abs/pii/S0004370215001198
- Run 100 times on 3/4 and participations accounted see if the generated structure is stable
- Start writing

### Activities

- Redownloaded data - the votes data indeed have been updated since last download
- Inconclusive which endpoint has higher quality data as they both are consistent within
- Read paper: Coalition structure generation: A survey
- Executed PAC algo with sampling of 3/4 of bills - the output structures are stable, but full of singletons when restriction loop is activated (not sure why)
- Wrote one paragraph about our data set

### Meeting Agenda: July 29th

- What to do with data inconsistency?
- What could have caused the singletons when sampling with restrictive loop enabled?
- Clarify optimized dynamic programming algorithm in the survey paper
- Is it meaningful to find solution that maximizes social welfare in our case?


## Week: July 12th - July 16th

### Goals

- Verify data pre-processing
- Tweak value function to count abstained as paritcipation and observe result change
- literature review: Coalition structure generation: A survey https://www.sciencedirect.com/science/article/abs/pii/S0004370215001198
- run 100 times on 3/4 and participations accounted see if the generated structure is stable


### Activities

- Went through data download and preprocessing code; fixed bug that produced excessive number of 0s in votes.csv
- Download additional data from bill summary endpoint to check sanity of member-bill vote data - inconsistency discovered
- Count "abstained" as participation - the results are mostly the same


### Meeting Agenda: July 17th

- How to resolve data inconsistency?
- More agorithms to implement?


## 2 Weeks: June 26th - July 11th

### Goals

- Coding and experimentation: increase size of average coalitipn for Knesset output
  - Fix value function to calculate majority only once per bill
  - Tweak sample size and value function
    - change value function to account for participation
    - change value function to account for how close the victory was
    - give losing coalition some small value


### Activities

- Pre-calculated valuations and coalition for every player and every bill
- Programmatically verified core stability of Knesset output
- Tried smaller sample size and the output average coalition size is still small - 1


### Meeting Agenda: July 12th

- How to use additional data?
- More tweaks?
- How to measure output partition's closeness to party affiliation?


## Week: June 20th - 25th

### Goals

- Coding: Implement PAC top covering algorithm (algorithm 1)

### Activities

- Completed first implementation of PAC top covering algorithm
- Executed the algorithm on knesset data

### Meeting Agenda: June 26th

- Clarification:
  - All preferences ranked after self is solely depends on size? Yes
  - How to treat missing preferences? They are worse than known options
  - If total for votes is more than against, but less than half the parliment, does the bill pass? Yes
  - Do we need to recalculate majority each time any player is removed? No
- Most output coalitions are of size 1
- Construct more test cases
- How to deal with uncertainty in testing?


## Week: June 10th - 20th

### Goals

- Literature review: understand PAC top covering algorithm
- Coding:
  - verify top covering algorithm efficiency
  - Check top covering algorithm weakly better off edge case

### Activities

- Added additional manual test cases provided by Alan
- Evaluated program efficiency: game with 142 players generated in: 14s; top covering algo completed in: 18s.

### Meeting Agenda: June 21th

- Clarify PAC top covering algorithm


## 2 Weeks: May 9th - May 22nd

### Goals

- Literature review: more on hedonic games
  - Handbook of Computational Social Choice, Chapter 15 Hedonic Games: http://procaccia.info/papers/comsoc.pdf
  - Researching with whom? stability and manipulation https://www.sciencedirect.com/science/article/abs/pii/S0304406803001277
- Coding: implement top covering algorithm


### Activities

- Read Handbook of Computational Social Choice, Chapter 15 Hedonic Games:http://procaccia.info/papers/comsoc.pdf
- Implemented top covering algorithm with handcrafted test cases
- Review & referenced relevant part of Researching with whom? Stability and manipulation: https://www.sciencedirect.com/science/article/abs/pii/S0304406803001277

### Meeting Agenda: June 10th

- Review top covering algorithm implementation


## Week: May 3rd - May 8th

### Goals

- Project setup
  - overleaf for doc collaboration: https://www.overleaf.com/project/5ccbf7fab95406669496706a
  - github for code versioning and review: https://github.com/weilu/coop-learning
- Literature review: understanding the key concepts and algorithms
  - PAC learning
  - Top Responsive games
  - Learning Hedonic Games algorithm 1: https://www.ijcai.org/proceedings/2017/0380.pdf

### Activities}

- Understood PAC learning basics: https://people.mpi-inf.mpg.de/~mehlhorn/SeminarEvolvability/ValiantLearnable.pdf
- Shattering and VC dimension: http://l2r.cs.uiuc.edu/Teaching/CS446-17/LectureNotesNew/colt/main.pdf

### Meeting Agenda: May 9th}

- Walk through algorithm 1, why it works
- Clarify questions from Learning Hedonic Games: https://www.ijcai.org/proceedings/2017/0380.pdf

