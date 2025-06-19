import random
import openai
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from encrypting import decrypt
from connection import dbConnectionHandle

openai.api_key = decrypt()
connection = None  # Will be set externally if needed

class algorithmPlayers:
    def __init__(self, host, userName, password, dbName, port):
        self.host = host
        self.userName = userName
        self.password = password
        self.dbName = dbName
        self.port = port

    class algorithmPlayer:
        def getChoice(self):
            pass

    class algorithmSelectionAutomated:
        def __init__(self, userAlgorithm, userRockChance, userPaperChance, userScissorsChance,
                        machineAlgorithm, machineRockChance, machinePaperChance, machineScissorsChance):
            self.userAlgorithm = userAlgorithm.lower()
            self.userRockChance = userRockChance
            self.userPaperChance = userPaperChance
            self.userScissorsChance = userScissorsChance
            self.machineAlgorithm = machineAlgorithm.lower()
            self.machineRockChance = machineRockChance
            self.machinePaperChance = machinePaperChance
            self.machineScissorsChance = machineScissorsChance

        def getChoicePlayer1(self):
            return algorithmPlayers.algorithmSelection(
                self.userAlgorithm, self.userRockChance, self.userPaperChance, self.userScissorsChance
            ).getChoice()

        def getChoicePlayer2(self):
            return algorithmPlayers.algorithmSelection(
                self.machineAlgorithm, self.machineRockChance, self.machinePaperChance, self.machineScissorsChance
            ).getChoice()

    class algorithmSelection:
        def __init__(self, machineAlgorithm, rockChance=None, paperChance=None, scissorsChance=None):
            self.machineAlgorithm = machineAlgorithm.lower()
            self.rockChance = rockChance
            self.paperChance = paperChance
            self.scissorsChance = scissorsChance

        def getChoice(self):
            if self.machineAlgorithm == "random":
                return algorithmPlayers.rngAlgorithm().getChoice()
            elif self.machineAlgorithm == "probability":
                return algorithmPlayers.probabilityAlgorithm(self.rockChance, self.paperChance, self.scissorsChance).getChoice()
            elif self.machineAlgorithm == "openai":
                return algorithmPlayers.openAIAlgorithm().getChoice()
            elif self.machineAlgorithm == "choppedai":
                return algorithmPlayers.choppedAI().getChoice()
            else:
                return "Rock"  # Default fallback

    class probabilityAlgorithm(algorithmPlayer):
        def __init__(self, rockChance, paperChance, scissorsChance):
            self.rockChance = rockChance
            self.paperChance = paperChance
            self.scissorsChance = scissorsChance

        def getChoice(self):
            total = self.rockChance + self.paperChance + self.scissorsChance
            if total == 0:
                return "Rock"
            scale = 255 / total
            r = self.rockChance * scale
            p = self.paperChance * scale
            rand = random.randint(1, 255)
            if rand <= r:
                return "Rock"
            elif rand <= r + p:
                return "Paper"
            else:
                return "Scissors"

    class rngAlgorithm(algorithmPlayer):
        def getChoice(self):
            return random.choice(["Rock", "Paper", "Scissors"])

    class openAIAlgorithm(algorithmPlayer):
        def getChoice(self):
            try:
                rows, _, _ = connection.readGameResults()
                prompt = "Past games:\n" + "\n".join(f"User {a}, AI {b}" for a, b in rows)
                prompt += "\nWhat's the best move to win next? Reply with: Rock, Paper, or Scissors."

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You're a rock-paper-scissors strategist."},
                        {"role": "user", "content": prompt}
                    ]
                )
                move = response.choices[0].message.content.strip().title()
                return move if move in ["Rock", "Paper", "Scissors"] else random.choice(["Rock", "Paper", "Scissors"])
            except Exception:
                return random.choice(["Rock", "Paper", "Scissors"])

    class choppedAI(algorithmPlayer):
        def __init__(self):
            self.choiceMap = {"r": 0, "p": 1, "s": 2}
            self.reverseMap = {0: "r", 1: "p", 2: "s"}
            self.counterMap = {0: 1, 1: 2, 2: 0}

        def getGameData(self):
            connect = connection.dbConnect()
            df = pd.read_sql_query("SELECT player1 as userchoice, player2 as machinechoice FROM RPSResults", connect)
            connect.close()
            if df.empty:
                return None
            df["userChoice"] = df["userchoice"].map(self.choiceMap)
            df["machineChoice"] = df["machinechoice"].map(self.choiceMap)
            return df.dropna()

        def trainModel(self, df):
            if df is None or len(df) < 5:
                return None
            x = df[["machineChoice"]]
            y = df["userChoice"]
            x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100)
            model.fit(x_train, y_train)
            return model

        def predictMove(self):
            df = self.getGameData()
            model = self.trainModel(df)
            if model is None:
                return random.choice(["r", "p", "s"])
            lastMachineMove = df["machineChoice"].iloc[-1]
            prediction = model.predict([[lastMachineMove]])[0]
            return self.reverseMap[self.counterMap[prediction]]

        def getChoice(self):
            return self.predictMove().title()
