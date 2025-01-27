# PhasmoPedia
Algorithm for Phasmophobia Radom custom settings or Random Difficulty

What data must be supplied?
Fixed data – “player_settings”, “ghost_settings”, and “contract_settings” “random_difficulty”
User input – do they want a random generated settings or a random difficulty
– if the user want a random generated settings they need to state how many settings that want generated (1-30)

What is required of the program?

1. Import the random module
2. Define three dictionaries, `player_settings`, `ghost_settings`, and `contract_settings`, which contain the various settings for each category.
3. Define a list called `random_difficulty`, which contains a list of various difficulty levels.
4. Start a while loop, which will keep running until the user inputs "quit"
5. Inside the while loop, ask the user to input one of the following: "random custom mode", "random difficulty", or "quit"
6. If the user inputs "quit", break out of the loop
7. If the user inputs "random difficulty", select a random difficulty level from the `random_difficulty` list and print it
8. If the user inputs "random custom mode", ask the user to input the number of random settings they want between 1 and 30.
9. Convert the user input to an integer and make sure it is within the range of 1 and 30.
10. For each setting requested, randomly select a category (player_settings, ghost_settings, contract_settings), then randomly select a setting from that category and print it.


