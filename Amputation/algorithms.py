import random
import openai # type: ignore
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as randomForestClassifier
from sklearn.model_selection import train_test_split as trainTestSplit
from encrypting import decrypt
from connection import dbConnectionHandle

openai.api_key = decrypt()

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
        def __init__(self, userAlgorithm, userRockChance, userPaperChance, userScissorsChance, machineAlgorithm, machineRockChance, machinePaperChance, machineScissorsChance):
            self.userAlgorithm = userAlgorithm
            self.userRockChance = userRockChance
            self.userPaperChance = userPaperChance
            self.userScissorsChance = userScissorsChance

            self.machineAlgorithm = machineAlgorithm
            self.machineRockChance = machineRockChance
            self.machinePaperChance = machinePaperChance
            self.machineScissorsChance = machineScissorsChance

        def getChoicePlayer1(self):
            if self.userAlgorithm == "PRO":
                return algorithmPlayers.probabilityAlgorithm(self.userRockChance, self.userPaperChance, self.userScissorsChance).getChoice()
            elif self.userAlgorithm == "RAN":
                return algorithmPlayers.rngAlgorithm().getChoice()
            elif self.userAlgorithm == "OPE":
                return algorithmPlayers.openAIAlgorithm().getChoice()
            elif self.userAlgorithm == "CHO":
                chopped_ai = algorithmPlayers.choppedAI(self.host, self.port, self.dbName, self.userName, self.password, self.machineAlgorithm)
                return chopped_ai.getChoice()
            else:
                return None

        def getChoicePlayer2(self):
            if self.machineAlgorithm == "PRO":
                return algorithmPlayers.probabilityAlgorithm(self.machineRockChance, self.machinePaperChance, self.machineScissorsChance).getChoice()
            elif self.machineAlgorithm == "RAN":
                return algorithmPlayers.rngAlgorithm().getChoice()
            elif self.machineAlgorithm == "OPE":
                return algorithmPlayers.openAIAlgorithm().getChoice()
            elif self.machineAlgorithm == "CHO":
                chopped_ai = algorithmPlayers.choppedAI(self.host, self.port, self.dbName, self.userName, self.password, self.machineAlgorithm)
                return chopped_ai.getChoice()
            else:
                return None

    class algorithmSelection:
        def __init__(self, machineAlgorithm, rockChance=None, paperChance=None, scissorsChance=None):
            self.machineAlgorithm = machineAlgorithm
            self.rockChance = rockChance
            self.paperChance = paperChance
            self.scissorsChance = scissorsChance

        def getChoice(self):
            if self.machineAlgorithm ==   "Random":
                return algorithmPlayers.rngAlgorithm().getChoice()
        
            elif self.machineAlgorithm == "Probability":
                return algorithmPlayers.probabilityAlgorithm(self.rockChance, self.paperChance, self.scissorsChance).getChoice()
            
            elif self.machineAlgorithm == "OpenAI":
                return algorithmPlayers.openAIAlgorithm().getChoice()
            
            elif self.machineAlgorithm == "ChoppedAI":
                chopped_ai = algorithmPlayers.choppedAI(self.host, self.port, self.dbName, self.userName, self.password, self.machineAlgorithm)
                return chopped_ai.getChoice()


    class probabilityAlgorithm(algorithmPlayer):
        def __init__(self, rockChance, paperChance, scissorsChance):
            self.rockChance = rockChance
            self.paperChance = paperChance
            self.scissorsChance = scissorsChance

        def getChoice(self):
            totalProbability = self.rockChance + self.paperChance + self.scissorsChance

            if totalProbability == 0:
                return "Probability Error"
            else:
                if totalProbability != 255:
                    scaleFactor = 255 / totalProbability
                    self.rockChance *= scaleFactor
                    self.paperChance *= scaleFactor
                    self.scissorsChance *= scaleFactor

            randNum = random.randint(1, 255)
# from sklearn.tree import DecisionTreeClassifier as decisionTreeClassifier
            if randNum <= self.rockChance:
                return "Rock"
            elif randNum <= self.rockChance + self.paperChance:
                return "Paper"
            else:
                return "Scissors"

    class rngAlgorithm(algorithmPlayer):
        def getChoice(self):
            return random.choice(["Rock", "Paper", "Scissors"])

    class openAIAlgorithm(algorithmPlayer):
        def getChoice(self):
            try:
                rows, col1, col2 = dbConnectionHandle.readGameResults()

                prompt = "Here are the past rock, paper and scissors games:\n"
                for col1, col2 in rows:
                    prompt += f"User {col1}, AI {col2}\n"
                
                prompt += "Based on these past games, what is the best move to do in order to win. Answer with one word: Rock, Paper or Scissors."

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": "You are a text analysis expert"},
                            {"role": "user", "content": prompt}]
                )

                decision = response.choices[0].message.content.strip().lower()

                if decision in ["rock", "paper", "scissors"]:
                    return decision.lower()
                else:
                    return random.choice(["Rock", "Paper", "Scissors"])
            except Exception as e:
                print(f"Error: {e}")
                return random.choice(["Rock", "Paper", "Scissors"])

    class choppedAI(algorithmPlayer):
        def __init__(self, host, port, db_name, user, password, machineAlgorithm):
            self.host = host
            self.port = port
            self.db_name = db_name
            self.user = user
            self.password = password
            self.engine = dbConnectionHandle.readGameResults(host, port, db_name, user, password)
            self.machineAlgorithm = machineAlgorithm

            self.choiceMapping = {"r": 0, "p": 1, "s": 2}
            self.reverseMapping = {0: "r", 1: "p", 2: "s"}
            self.counterMove = {0: 1, 1: 2, 2: 0}  # Rock -> Paper, Paper -> Scissors, Scissors -> Rock

        def getGameData(self):
            df = pd.read_sql_query("SELECT userchoice, machinechoice FROM RPSResultsArchive", self.engine)
            df.dropna(inplace=True)

            if df.empty:
                print("(debug) No data in DB")
                return None
            
            df["userChoice"] = df["userchoice"].map(self.choiceMapping)
            df["machineChoice"] = df["machinechoice"].map(self.choiceMapping)

            return df

        def trainModel(self):
            df = self.getGameData()
            if df is None or len(df) < 5:
                print("(debug) Not enough data to train the model")
                return None

            x = df[["machineChoice"]].values
            y = df[["userChoice"]].values
            x_train, _, y_train, _ = trainTestSplit(x, y, test_size=0.2, random_state=42)
            x_train, x_test, y_train, y_test = trainTestSplit(x, y, test_size=0.2, random_state=42)

            model = randomForestClassifier(n_estimators=100)
            model.fit(x_train, y_train.ravel())
            return model

        def predictMove(self):
            model = self.trainModel()

            if model is None:
                print("AI is choosing randomly")
                return random.choice(["r", "p", "s"])

            df = self.getGameData()
            lastMMove = df["machineChoice"].values[-1] if df is not None else random.choice([0, 1, 2])

            prediction = model.predict([[lastMMove]])[0]
            print(f"AI is predicting {self.reverseMapping[prediction]}")

            bestMove = self.reverseMapping[self.counterMove[prediction]]
            print(f"(DEBUG) AI selects: {bestMove}")
            return bestMove

        def getChoice(self):
            machineChoice = self.predictMove()
            return machineChoice