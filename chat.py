from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import logging
import sys

# Enable info level logging
# logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    'ChatBot',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ]
)

def get_answer(inp):
    print("CHATBOT :: processing:", inp)
    try:
        r = chatbot.get_response(inp)
    except Exception as e: 
        print(str(e))
        return "Error processing message"

    print("CHATBOT :: responded:", r)
    return r


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "train":
        chatbot.set_trainer(ChatterBotCorpusTrainer)
        chatbot.train('chatterbot.corpus.english')
    else:
        chatbot.input_adapter="chatterbot.input.TerminalAdapter"
        chatbot.output_adapter="chatterbot.output.TerminalAdapter",
        while True:
            try:
                bot_input = chatbot.get_response(None)

            except (KeyboardInterrupt, EOFError, SystemExit):
                break
