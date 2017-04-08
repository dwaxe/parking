    ______          _     _                  __  
    | ___ \        | |   | |                /  | 
    | |_/ / __ ___ | |__ | | ___ _ __ ___   `| | 
    |  __/ '__/ _ \| '_ \| |/ _ \ '_ ` _ \   | | 
    | |  | | | (_) | |_) | |  __/ | | | | | _| |_
    \_|  |_|  \___/|_.__/|_|\___|_| |_| |_| \___/
    ---------------------------------------------            


## How to use the website:

* Visit [this link](https://parking-dwaxe.c9users.io) and log in with username `ridecell` and password `ridecell` (registration works, but displays an error message).
* There should be a map displaying parking spots. Currently reserved parking spots are labeled 'R', and open ones 'P'
* Enter an address in the search bar at the top to center the map on it
* Click a parking spot on the map to view its details and reserve it (You can only view spots you own or spots nobody owns)
* If click on a parking spot you currently have reserved, you can delete your reservation


## Code located [here](https://preview.c9users.io/dwaxe/parking/)

* C9 IDE for development and hosting, Bootstrap and templates for html, Google Maps API for the map, Django for all the logic
* I implemented reservations within the ParkingSpot model, so it only supports one reservation per parking lot


## Things I didn't implement or didn't fix for lack of time:

This is my first time writing a Django application, and I have to admit it's not pretty.
I spent half my time working on this application in fits and starts as I learned
some of the Dos and Donts of Django development. Clearly I have a lot to learn about Django

* No tests
* No documentation
* Registration works, but there's a jarring error message at the end that I haven't squashed
* You can't view the details of a spot owned by someone else


    ______          _     _                  _____ 
    | ___ \        | |   | |                / __  \
    | |_/ / __ ___ | |__ | | ___ _ __ ___   `' / /'
    |  __/ '__/ _ \| '_ \| |/ _ \ '_ ` _ \    / /  
    | |  | | | (_) | |_) | |  __/ | | | | | ./ /___
    \_|  |_|  \___/|_.__/|_|\___|_| |_| |_| \_____/
    -----------------------------------------------            
            
                                               
## Problem Statement

The city's parking agency (SFMTA) wants to start a new parking valet service which will 
complement the parking spot reservation system built as part of Problem #1. Users enter 
the address that they will be arriving at, and a valet should be ready to meet them when they 
arrive and pick up their car to park it. SFMTA's goals are to service the maximum number of 
customers per valet and to maximize usage of parking spots.


## Remarks

This is an NP-Hard optimization problem. It is a variant of [Multiprocessor scheduling](https://www.wikiwand.com/en/Multiprocessor_scheduling)
or [Job shop scheduling](https://www.wikiwand.com/en/Job_shop_scheduling). Because
our solution is bound to be suboptimal, we will go with a greedy algorithm to minimize
computation. [More complicated solutions exist,](https://www.wikiwand.com/en/Job_shop_scheduling#/Offline_makespan_minimization)
but this is good enough for the SFMTA.


## Algorithm

Inputs: Valet locations (V), Customer dropoff locations and times (C), Parking spot locations (P)

* We will use a priority queue of all Valet-Customer combinations. O(V*C) memory
* The priority function will be estimated time of completion of the valet dispatch.
* P(V, C) = min(earliest time V can get to C location, C time) + average time distance to 3 nearest open Parking Spots. O(P) computational complexity
* We can't be certain whether the nearest open Parking Spot will be reserved in the future, so we hedge by averaging the 3 nearest open Parking Spots at the time.
* We sort priorities from earliest to latest
* We assign Valet-Customer interactions by looping through the priority queue. If both the Valet and Customer are not yet assigned, we assign them to each other. O(V*C) computational complexity
* Each Valet-Customer assignment is a reservation in our system in Problem 1
* Every time a new Customer request comes in we add all the Valet priorities to the queue. O(V) computational complexity
* Every time a Valet starts an assignment we recalculate their priorities. O(C) computational complexity
* If the updated priority queue calls for a new set of Valet-Customer interactions, we reassign to the new, more efficient schedule

This algorithm tries to minimize the time spent waiting by customers. It handles situations of a closer
customer requesting a Valet by recalculating at each new request. It will only reassign if switching
the Valet to the new request actually has a sooner priority.

## Architecture

Implement the priority queue in models.py with a `class Priority(models.Model)`
with fields priority (DateTimeField), valet (ForeignKey User), customer (ForeignKey User),
reservation (ForeignKey ParkingSpot).



