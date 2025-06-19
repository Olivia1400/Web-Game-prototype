import gradio as gr
import openai 
from game import rpsGame
from connection import dbConnectionHandle as db
from encrypting import decrypt
from css import customCSS

openai.api_key = decrypt()

connectionDetails = open("databricksConnectionDetails.txt").read().splitlines()
connection = db(
    connectionDetails = connectionDetails,
    server_hostname = connectionDetails[0],
    http_path = connectionDetails[1],
    access_token = connectionDetails[2])

def showProbabilityOptions(algorithm):
    return [gr.update(visible=(algorithm == "Probability"))] * 3

is_logged_in = gr.State(value=False)
current_user = gr.State(value=None)

def handle_login(username, password):
    result, userID = connection.loginINIT(username, password)
    if "success" in result.lower():
        connection.userID = userID # ✅ Set the userID on the connection
        return True, username, gr.update(visible=True), result
    return False, None, gr.update(visible=False), result


with gr.Blocks(title="Rock Paper Scissors", css=customCSS()) as app:
    with gr.Tab("Login"):
        gr.Markdown("### Login\nEnter your credentials to access the Rock Paper Scissors game.")
        loginUserName = gr.Textbox(label="Username")
        loginUserPassword = gr.Textbox(label="Password", type="password")
        loginOutput = gr.Textbox(label="", interactive=False)
        buttonLogin = gr.Button("Login")

    with gr.Tab("Signup"):
        gr.Markdown("### Signup\nCreate a new account to begin playing.")
        gr.Markdown('Username must be at least 3 characters\nPassword at least 6 characters long and contain 1 number and 1 capital letter.')
        signupUserName = gr.Textbox(label="Username")
        signupUserPassword = gr.Textbox(label="Password", type="password")
        signupOutput = gr.Textbox(label="", interactive=False)
        buttonSignup = gr.Button("Signup")

    main_app_container = gr.Column(visible=False)

    def handle_login(username, password):
        result, userID = connection.loginINIT(username, password)
        if "success" in result.lower():
            connection.userID = userID # Track logged-in user
            print(f"[DEBUG] Logged in userID: {connection.userID}")
            return True, username, gr.update(visible=True), result
        return False, None, gr.update(visible=False), result

    buttonLogin.click(
        fn=handle_login,
        inputs=[loginUserName, loginUserPassword],
        outputs=[is_logged_in, current_user, main_app_container, loginOutput]
    )

    buttonSignup.click(
        fn=lambda u, p: connection.signupSystemVerify(u, p),
        inputs=[signupUserName, signupUserPassword],
        outputs=signupOutput
    )

    with main_app_container:
        gr.Markdown("## Welcome to Rock Paper Scissors 🎮\nUse the tabs to play, simulate AI battles, or view the leaderboards.")

        with gr.Tab("Play"):
            gr.Markdown("### Instructions\n1. Choose Rock, Paper, or Scissors.\n2. Select the opponent’s AI.\n3. Adjust probabilities (if applicable).\n4. Press Play to compete!")
            userChoice = gr.Radio(choices=["Rock", "Paper", "Scissors"], value="Rock", show_label=False)
            machineAlgorithm = gr.Dropdown(choices=["Random", "Probability", "OpenAI", "ChoppedAI"], show_label=False)
            rockChance = gr.Slider(0, 255, value=0, label="Rock Chance", visible=False)
            paperChance = gr.Slider(0, 255, value=0, label="Paper Chance", visible=False)
            scissorsChance = gr.Slider(0, 255, value=0, label="Scissors Chance", visible=False)
            playGame = gr.Button("Play")
            gameOutput = gr.Textbox(show_label=False)
            
            machineAlgorithm.change(fn=showProbabilityOptions, inputs=machineAlgorithm, outputs=[rockChance, paperChance, scissorsChance])
            playGame.click(fn=rpsGame.rockPaperScissors, inputs=[userChoice, machineAlgorithm, rockChance, paperChance, scissorsChance], outputs=gameOutput)

        with gr.Tab("Automation"):
            gr.Markdown("### Instructions\nRun up to 100,000 AI vs AI matches. Customize player strategies and view the results!")
            automationAmount = gr.Slider(minimum=1, maximum=100000, step=1, label="Number of Games")
            
            gr.Markdown("#### Player 1 AI Setup")
            player1Algorithm = gr.Dropdown(choices=["Random", "Probability", "ChoppedAI"])
            player1RockChance = gr.Slider(0, 255, label="Rock Chance", visible=False)
            player1PaperChance = gr.Slider(0, 255, label="Paper Chance", visible=False)
            player1ScissorsChance = gr.Slider(0, 255, label="Scissors Chance", visible=False)
            player1Algorithm.change(fn=showProbabilityOptions, inputs=player1Algorithm, outputs=[player1RockChance, player1PaperChance, player1ScissorsChance])
            
            gr.Markdown("#### Player 2 AI Setup")
            player2Algorithm = gr.Dropdown(choices=["Random", "Probability", "ChoppedAI"])
            player2RockChance = gr.Slider(0, 255, label="Rock Chance", visible=False)
            player2PaperChance = gr.Slider(0, 255, label="Paper Chance", visible=False)
            player2ScissorsChance = gr.Slider(0, 255, label="Scissors Chance", visible=False)
            player2Algorithm.change(fn=showProbabilityOptions, inputs=player2Algorithm, outputs=[player2RockChance, player2PaperChance, player2ScissorsChance])

            automation = gr.Button("Run Automation")
            automatedGameOutput = gr.Textbox(show_label=False)

            automation.click(
                fn=rpsGame.rockPaperScissorsAutomated,
                inputs=[automationAmount, player1Algorithm, player2Algorithm,
                        player1RockChance, player1PaperChance, player1ScissorsChance,
                        player2RockChance, player2PaperChance, player2ScissorsChance],
                outputs=automatedGameOutput
            )

        with gr.Tab("Leaderboards"):
            gr.Markdown("### View the Top 10 Casual Players 👑")
            leaderboardList = gr.List(
                label="Leaderboard Top 10",
                value=connection.getLeaderboardTop10(),
                show_label=True,
                show_row_numbers=True,
                row_count=10,
                interactive=False
            )

if __name__ == "__main__": 
    app.launch(share=True)
