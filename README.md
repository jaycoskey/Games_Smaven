# Smaven README

## Description
Words that can be played in games such as Scrabble need to meet a few constraints:
* Board constraint: Letters (a.k.a. tiles) played must fit on the board, must form a contiguous sequence of tiles, etc.
* Rack constraint: Letters played come from the players "rack". 
* Dictionary constraint: Words formed must be in the dictionary. (The Official Scrabble Players Dictionary, in Scrabble tournaments.)

A sensible way to find words that meet these constraints is to use a data structure that allows you to search the board square by square, asking for each square, "What letters can I play on this square, and what words can be formed from them?". The DAGGAD (see https://en.wikipedia.org/wiki/GADDAG) is a data structure designed for this type of search. (The starting square in such a search is commonly called a "hook".) The DAGGAD is a trie (see https://en.wikipedia.org/wiki/Trie), in which letter sequences from the root to a leaf contain the letters of a word, but in a particular order, as shown below.
* e+xplain
* xe+plain
* pxe+lain
* lpxe+ain
* alpxe+in
* ialpxe+n
* nialpxe

Note that the GADDAG would contain 7 sequences for the word "explain".

This repo contains a program (in development) to find words playable on a given board, with a given rack, and a given dictionary.
It might be expanded to allow human vs computer competition, or even use machine learning to hone the computer's strategy.

## Design

### Commands and options

| Command                     | Args                   | Notes                                              |
| --------------------------- | ---------------------- | -------------------------------------------------- |
| Help                        | --help                 |                                                    |
| Verbose                     | -v --verbose           |                                                    |
| Specify config file         | -c --config CONFIG     |                                                    |
| Set display mode to text    | -t --text              |                                                    |
| Set display mode to GUI     | -g --gui               |                                                    |
| Specify layout              | -l --layout LAYOUT     | LAYOUT refers to file or config entry (with '@')   |
| Command: Search             | search                 | Search for words & show results                    |
|   Specify board             |   -b --board BOARD     | BOARD refers to file or config entry (with '@')    |
|   Specify (letters in rack) |   -r --rack RACK       | RACK is a string, such as "kwyjibo"                |
| Commnad: Experiment         | experiment             | Load/Save games, inspect GTree data structure, etc.|
| Command: Players            | players (-hh\|-hc\|-cc)| Play games (Human vs Human, etc.)                  |
| Command: AI                 | ai                     | Develop a computer strategy via training           |

### Console version
* Design of program to find playable words for a given Board/Rack/Dictionary? CLI arguments?
* If there will be a text (i.e., ASCII) version, how to display square types along with letters played?

### GUI version
* GUI layout?
* Colors?
  * Two players:   2 of aquamarine, blush pink, dolly
  * Three players: 3 of aquamarine, blush pink, dolly
  * Four+ players: Above + aqua, malibu, mint green, fuschia, vivid tangerine, yellow

| Hex | Color name | Brightness | Notes                       |
| --- | -----------| ---------- | ----------------------------|
| #00_00_00| BLACK           |0|                              |
| #00_00_7f| navy blue       |1| dark blue                    |
| #00_00_ff| BLUE            |2|                              |
|          |                 | |                              |
| #00_7f_00| dark lime green |1| japanese laurel              |
| #00_7f_7f| teal            |2| dark cyan                    |
| #00_7f_ff| azure radiance  |3|                              |
|          |                 | |                              |
| #00_ff_00| GREEN           |2|                              |
| #00_ff_7f| spring green    |3| lime green                   |
| #00_ff_ff| AQUA            |4|                              |
| ======== | =============== |=| ============================ | 
| #7f_00_00| maroon          |1| dark red                     |
| #7f_00_7f| eggplant        |2| fresh eggplant, dark magenta |
| #7f_00_ff| violet          |3| electric violet              |
|          |                 | |                              |
| #7f_7f_00| olive           |2|                              |
| #7f_7f_7f| gray            |3|                              |
| #7f_7f_ff| malibu          |4| very light blue              |
|          |                 | |                              |
| #7f_ff_00| chartreuse      |3|                              |
| #7f_ff_7f| mint green      |4| very light lime green        |
| #7f_ff_ff| aquamarine      |5| very light cyan              |
| ======== | =============== |=| ============================ |
| #ff_00_00| RED             |2|                              |
| #ff_00_7f| rose            |3|                              |
| #ff_00_ff| FUSCHIA         |4| magenta                      |
|          |                 | |                              |
| #ff_7f_00| orange          |3| flush orange                 |
| #ff_7f_7f| tangerine       |4| vivid tangerine              |
| #ff_7f_ff| blush pink      |5|                              |
|          |                 | |                              |
| #ff_ff_00| YELLOW          |4|                              |
| #ff_ff_7f| dolly           |5| very light yellow            |
| #ff_ff_ff| WHITE           |6|                              |

### Implementation
* Should the GADDAG (class GTree) be compressed?

## Task backlog
* TODO: Complete search feature
* TODO: BTree unit tests
* TODO: Search tests (See below)
* TODO: Compute score
* TODO: GTree.find_words efficiency. Any duplicate evaluation of states that can be efficiently removed?
* TODO: Support (text) human vs human console play: move, swap, pass, resign.
* TODO: Support game state serialization/deserialization (incl. turn history)
* TODO: Implement GUI versions
* TODO: Support human vs computer game play. (Initially, computer chooses highest-scoring move)
* TODO: Distributed system with clients & server
* TODO: Hex board?
* TODO: AI feature (See below)

### Search tests
* TODO: Search test (fill contiguous): Board:"aa.....k", Rack:adrrvyz. Find aardvark
* TODO: Search test (fill contiguous with blank): Board:"aa.....k", Rack:rd_aryz. Find aardvark
* TODO: Any search test that finds words should find at least those words when a letter tile is replaced by a blank.
* TODO: Search test (noncontiguous): Board:ear.hen.are, Rack:xtywz. Find "earthenware"
* TODO: Search test (board edge): Board:"^liqui", Rack:'dateion'. Find liquid, liquidate, liquidation
* TODO: Search test (crossing words): Board:"zebra", Rack:ooca. Find zoo, cab, aa (x2) 
* TODO: Search test (parallel word): Board:"name", "wend", Rack:enox. Find (primary)oxen, (secondaries)now, axe, men, end

### AI feature: Training computer strategy
* Evolve computer strategy via Computer vs Computer play
  * Note: Choosing the highest-scoring move in every round is not the best strategy.
    * For example, playing a BLANK tile to get one additional point is probably suboptimal.
* Potential turn features for reinforcement learning:
  * Points earned
  * Expected value of opponent's next turn
    * Sample "best" move from 100 samples taken from the distribution of remaining files
    * For "best", start by assuming that opponent plays highest-scoring move
  * Proportion of vowels in rack
  * Is BLANK in rack / on board / in bag? (Scrabble: 2)
  * Is S in rack / on board / in bag? (Scrabble: 4)
  * Is J in rack / on board / in bag? (Scrabble: 1)
  * Is Q in rack / on board / in bag? (Scrabble: 1)
  * Is X in rack / on board / in bag? (Scrabble: 1)
  * Is Z in rack / on board / in bag? (Scrabble: 1)
  * Number of tiles remaining in bag (Scrabble: 100, WWF: 94)
  * Count of Qs not yet played
  * Count of Us not yet played
  * Distances (perpendicular, parallel) to closest triple word square for opponent's next move
  * Distances (perpendicular, parallel) to closest double word square for opponent's next move
  * Distances (perpendicular, parallel) to closest triple letter square for opponent's next move
  * Distances (perpendicular, parallel) to closest double letter square for opponent's next move
  * Etc.
