# Chess-ai  
using alpha beta algorithm create ai chess  
This is fully feature chess app using pygame library  
# Features  
* Clean GUI with a lot of menus for ease of use.  
* Allows users to make only valid move, does not allow users to make moves that puts the user's king at check.  
* Detects check, checkmate, stalemate and informs user.  
* Supports things like castling, pawn promotion, enpassent etc.  
* Has single player model  
# Algorithm  
we use alpha-beta algorithm combine logistic regression for predict next move  
logistic regression will reduce 50% number of posible moves  
After that, alpha-beta will choose best move  
# How to run  
make sure you cloned my project and have python 3  
## Set up library  
`cd chess_ai`  
`python install -r requirement.txt`  

## Run
`python run.py`

# Training
We run training algorithm in colab and save model to predict.  
Linear model saved in chess_ai/ai/agents/Model/linear_estimator.zip  
neural model saved in chess_ai/ai/agents/Model/dnn_estimator.zip  
To tranform dataset to vector run chess_ai.ai.agents.data_transform.py  
to train linear model run chess_ai.ai.agents.load_data.py  
