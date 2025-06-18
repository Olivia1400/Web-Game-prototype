from algorithms import algorithmPlayers
from connection import dbConnectionHandle

connectionDetails = open("databricksConnectionDetails.txt").read().splitlines()

connection = dbConnectionHandle(
    connectionDetails = connectionDetails,
    server_hostname = connectionDetails[0],
    http_path = connectionDetails[1],
    access_token = connectionDetails[2]
)



## || This class handles the Rock-Paper-Scissors game logic, including user and machine choices  ||

class rpsGame:
    def rockPaperScissors(userChoice, machineAlgorithm, rockChance, paperChance, scissorsChance):
        userAlgorithm = "HUM"

        machineChoice = algorithmPlayers.algorithmSelection(machineAlgorithm, rockChance, paperChance, scissorsChance).getChoice()

        if userChoice not in ["Rock", "Paper", "Scissors"]:
            return f"Invalid user choice: {userChoice}"

        if machineChoice not in ["Rock", "Paper", "Scissors"]:
            return f"Invalid machine choice: {machineChoice}"

        userChoiceDatabase = userChoice[0].lower()
        machineChoiceDatabase = machineChoice[0].lower()

        machineAlgorithm = machineAlgorithm[:3].upper()

        if (userChoice == "Rock" and machineChoice == "Paper") or (userChoice == "Paper" and machineChoice == "Scissors") or (userChoice == "Scissors" and machineChoice == "Rock"):
            dbConnectionHandle.insertGameResult(userChoiceDatabase, machineChoiceDatabase, userID= dbConnectionHandle.userIDcheck())
            return f"Loss, the machine chose {machineChoice}."
        elif userChoice == machineChoice:
            dbConnectionHandle.insertGameResult(userChoiceDatabase, machineChoiceDatabase, userID= dbConnectionHandle.userIDcheck())
            return f"Draw, the machine chose {machineChoice}."
        else:
            dbConnectionHandle.insertGameResult(userChoiceDatabase, machineChoiceDatabase, userID= dbConnectionHandle.userIDcheck())
            return f"Victory, well done! The machine chose {machineChoice}."

    def rockPaperScissorsAutomated(automationAmount, player1Algorithm, player2Algorithm, player1RockChance, player1PaperChance, player1ScissorsChance, player2RockChance, player2PaperChance, player2ScissorsChance):
        userAlgorithm = player1Algorithm[:3].upper()
        machineAlgorithm = player2Algorithm[:3].upper()

        if (player1Algorithm == "Probability" and sum([player1RockChance, player1PaperChance, player1ScissorsChance]) == 0) or (player2Algorithm == "Probability" and sum([player2RockChance, player2PaperChance, player2ScissorsChance]) == 0):
            return "Either Player 1 or Player 2 has their total probability as 0. Adjust the probabilities to be greater than 0."
        else:
            for _ in range(automationAmount):

                player1Choice = algorithmPlayers.algorithmSelectionAutomated(
                    userAlgorithm,
                    player1RockChance,
                    player1PaperChance,
                    player1ScissorsChance,
                    machineAlgorithm,
                    player2RockChance,
                    player2PaperChance,
                    player2ScissorsChance
                ).getChoicePlayer1()

                player2Choice = algorithmPlayers.algorithmSelectionAutomated(
                    userAlgorithm,
                    player1RockChance,
                    player1PaperChance,
                    player1ScissorsChance,
                    machineAlgorithm,
                    player2RockChance,
                    player2PaperChance,
                    player2ScissorsChance
                ).getChoicePlayer2()

                if player1Choice is None or player2Choice is None:
                    return f"Skipping iteration due to None choice: player1Choice={player1Choice}, player2Choice={player2Choice}"

                userChoiceDatabase = player1Choice[0].lower()
                machineChoiceDatabase = player2Choice[0].lower()
                dbConnectionHandle.insertGameResult(userChoiceDatabase, machineChoiceDatabase, userID=dbConnectionHandle.userIDcheck())

            return "The results have been generated."

