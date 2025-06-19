from algorithms import algorithmPlayers
from connection import dbConnectionHandle


connectionDetails = open("databricksConnectionDetails.txt").read().splitlines()
connection = dbConnectionHandle(
    connectionDetails=connectionDetails,
    server_hostname=connectionDetails[0],
    http_path=connectionDetails[1],
    access_token=connectionDetails[2]
)

# Optional: inject global reference into algorithmPlayers
algorithmPlayers.connection = connection

class rpsGame():
    @staticmethod
    def rockPaperScissors(userChoice, machineAlgorithm, rockChance, paperChance, scissorsChance):
        machineChoice = algorithmPlayers.algorithmSelection(
            machineAlgorithm,
            rockChance,
            paperChance,
            scissorsChance
        ).getChoice()
        userID = dbConnectionHandle.userIDcheck
        if userChoice not in ["Rock", "Paper", "Scissors"]:
            return f"Invalid user choice: {userChoice}"
        if machineChoice not in ["Rock", "Paper", "Scissors"]:
            return f"Invalid machine choice: {machineChoice}"

        uc = userChoice[0].lower()
        mc = machineChoice[0].lower()
        connection.insertGameResult(uc, mc, userID)


        if userChoice == machineChoice:
            return f"Draw, the machine chose {machineChoice}."
        elif (
            (userChoice == "Rock" and machineChoice == "Paper") or
            (userChoice == "Paper" and machineChoice == "Scissors") or
            (userChoice == "Scissors" and machineChoice == "Rock")
        ):
            return f"Loss, the machine chose {machineChoice}."
        else:
            return f"Victory, well done! The machine chose {machineChoice}."

    @staticmethod
    def rockPaperScissorsAutomated(
        automationAmount,
        player1Algorithm,
        player2Algorithm,
        player1RockChance,
        player1PaperChance,
        player1ScissorsChance,
        player2RockChance,
        player2PaperChance,
        player2ScissorsChance
    ):
        # Quick validation
        if player1Algorithm == "Probability" and sum([player1RockChance, player1PaperChance, player1ScissorsChance]) == 0:
            return "Player 1's total probability is zero. Adjust values."
        if player2Algorithm == "Probability" and sum([player2RockChance, player2PaperChance, player2ScissorsChance]) == 0:
            return "Player 2's total probability is zero. Adjust values."

        for _ in range(automationAmount):
            logic = algorithmPlayers.algorithmSelectionAutomated(
                player1Algorithm,
                player1RockChance,
                player1PaperChance,
                player1ScissorsChance,
                player2Algorithm,
                player2RockChance,
                player2PaperChance,
                player2ScissorsChance
            )
            p1 = logic.getChoicePlayer1()
            p2 = logic.getChoicePlayer2()

            if p1 is None or p2 is None:
                continue  # Skip invalid rounds

            uc = p1[0].lower()
            mc = p2[0].lower()
            connection.insertGameResult(uc, mc, connection.userIDcheck())
        return "Automated game results generated successfully."
