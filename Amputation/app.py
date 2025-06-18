import gradio as gr # type: ignore
import subprocess
import sys
import openai 
from game import rpsGame
#from algorithms import algorithmPlayer, algorithmSelection, algorithmSelectionAutomate
from connection import dbConnectionHandle as db
from encrypting import decrypt


openai.api_key = decrypt()




def showProbabilityOptions(machineAlgorithm):
    visibility = machineAlgorithm == "Probability"
    return [gr.update(visible=visibility)] * 3

def showProbabilityOptionsPlayer1(player1Algorithm):
    visibility = player1Algorithm == "Probability"
    return [gr.update(visible=visibility)] * 3

def showProbabilityOptionsPlayer2(player2Algorithm):
    visibility = player2Algorithm == "Probability"
    return [gr.update(visible=visibility)] * 3

with gr.Blocks(title="Rock Paper Scissors") as app:
    gr.Markdown("Rock Paper Scissors Game")
    
    with gr.Tab("Play"):
        gr.Markdown("Choose your move")
        userChoice = gr.Radio(choices=["Rock", "Paper", "Scissors"], value="Rock", show_label=False)
        
        gr.Markdown("Opponent Tweaks")
        machineAlgorithm = gr.Dropdown(choices=["Random", "Probability", "OpenAI", "ChoppedAI"], show_label=False)
        rockChance = gr.Slider(0, 255, value=0, label="Rock Chance", step=1, visible=False)
        paperChance = gr.Slider(0, 255, value=0, label="Paper Chance", step=1, visible=False)
        scissorsChance = gr.Slider(0, 255, value=0, label="Scissors Chance", step=1, visible=False)

        gr.Markdown("Game Output")
        gameOutput = gr.Textbox(show_label=False)
        playGame = gr.Button("Play")

        machineAlgorithm.change(fn=showProbabilityOptions, inputs=machineAlgorithm, outputs=[rockChance, paperChance, scissorsChance])
        
        playGame.click(fn=rpsGame.rockPaperScissors, inputs=[userChoice, machineAlgorithm, rockChance, paperChance, scissorsChance], outputs=gameOutput)

    with gr.Tab("Automation"):
        gr.Markdown("Automation Game Amount")
        automationAmount = gr.Slider(minimum=1, maximum=100000, step=1, show_label=False)

        gr.Markdown("Player 1 Algorithm", show_label=False)
        player1Algorithm = gr.Dropdown(choices=["Random", "Probability", "ChoppedAI"], show_label=False)
        player1RockChance = gr.Slider(0, 255, value=0, label="Rock Chance", step=1, visible=False)
        player1PaperChance = gr.Slider(0, 255, value=0, label="Paper Chance", step=1, visible=False)
        player1ScissorsChance = gr.Slider(0, 255, value=0, label="Scissors Chance", step=1, visible=False)
        player1Algorithm.change(fn=showProbabilityOptionsPlayer1, inputs=player1Algorithm, outputs=[player1RockChance, player1PaperChance, player1ScissorsChance])

        gr.Markdown("Player 2 Algorithm", show_label=False)
        player2Algorithm = gr.Dropdown(choices=["Random", "Probability", "ChoppedAI"], show_label=False)
        player2RockChance = gr.Slider(0, 255, value=0, label="Rock Chance", step=1, visible=False)
        player2PaperChance = gr.Slider(0, 255, value=0, label="Paper Chance", step=1, visible=False)
        player2ScissorsChance = gr.Slider(0, 255, value=0, label="Scissors Chance", step=1, visible=False)
        player2Algorithm.change(fn=showProbabilityOptionsPlayer2, inputs=player2Algorithm, outputs=[player2RockChance, player2PaperChance, player2ScissorsChance])

        gr.Markdown("Game Output")
        automatedGameOutput = gr.Textbox(show_label=False)

        automation = gr.Button("Automation")
        automation.click(fn=rpsGame.rockPaperScissorsAutomated, 
            inputs=[automationAmount, 
                    player1Algorithm, player2Algorithm, 
                    player1RockChance, player1PaperChance, player1ScissorsChance, 
                    player2RockChance, player2PaperChance, player2ScissorsChance], 
            outputs=automatedGameOutput)

    with gr.Tab("Login"):
        gr.Markdown("Login")
        loginUserName = gr.Textbox(label="Username", show_label=True)
        loginUserPassword = gr.Textbox(label="Password", type="password", show_label=True)
        loginOutput = gr.Textbox(label="Login Status", show_label=False, interactive=False)
        buttonLogin = gr.Button("Login")
        buttonLogin.click(
            fn=lambda loginUserName, loginUserPassword: db.loginINIT('', loginUserName, loginUserPassword),
            inputs=[loginUserName, loginUserPassword],
            outputs=loginOutput
        )
        
    with gr.Tab("Signup"):
        gr.Markdown("Signup")
        signupUserName = gr.Textbox(label="Username", show_label=True)
        signupUserPassword = gr.Textbox(label="Password", type="password", show_label=True)
        signupOutput = gr.Textbox(label="Signup Status", show_label=False, interactive=False)
        buttonSignup = gr.Button("Signup")
        buttonSignup.click(
            fn=lambda signupUserName, signupUserPassword: db.signupSystemVerify(signupUserName, signupUserPassword),
            inputs=[signupUserName, signupUserPassword],
            outputs=signupOutput
        )
    with gr.Tab("Leaderboards"):
        with gr.Tab("Casual Leaderboards"):
            with gr.Tab("Leaderboard Top 10"):
                gr.Markdown("Top 10")
                leaderboardList = gr.List(label=" Leaderboard Top 10",
                    value= db.getLeaderboardTop10(connection),
                    show_label=True, show_row_numbers=True, row_count=10,
                    interactive=False, visible=True)
                
                
    
'''        with gr.Tab("Competitive Leaderboards"):
            with gr.Tab("Leaderboard Top 10"):'''

if __name__ == "__main__": 
    command = [
        sys.executable,
        '-m',
        'pip',
        'install',
        '--requirement',
        'requirements.txt',
    ]
    subprocess.run(command, text=True)
    app.launch()