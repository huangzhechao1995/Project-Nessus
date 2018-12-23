#Project-Nessus

"""
Created on Thu Nov  8 14:20:51 2018

@author: Zhechao (Andrew) Huang, Jixin Wang
"""

Machine-Learning Assisted Product Configuration. The model takes in excel format data, which is processed from production configuration in html format. The output is the predicted configuration. The iterative approach allows to adjust step size (the number of data fields that are entered before our algorithms start predicting future answers) and predicted legth (how many predcitions are given at a time). 

#Model Structure
To run the code, simply call main.py with arguments in the terminal. Below are detailed explanation for our model structure.

1. model.py
Store implementation details for Scanning-based models, including KNN and Distance-based frequency method. 

Potential model adjustment in the future:
KNN:
K: default setting "30"
Distance Metric: default setting "Manthattan"

2. para_models.py 
Store implementation details for Coefficient-based models, including CART and Random Forest method. 

Requires to train and store the coefficient first before making prediction. 

3. util.py
Set argument and defaul argument. 

'--filename', default="Featureset01.xlsx"
'--root', default="path where the xlsx file is"
'--method, default="KNN", other options include : "CART", "RF", "Frequency"
'--test_split', default=4000, how to split test and training data, main purpose is for algorithm evaluation 
'--update_step', default= 5, the number of data fields that are entered before our algorithms start predicting future answers
'--pred_length', default=5, how many predcitions are given at a time
'--instant_update',type=bool, default=False
'--train_flag',type=bool, default=True, to train, validate and store the model, only for "CART" and "RF"
'--test_flag', type=bool, default=False, to test model, i.e. give prediction 
'--print_prediction',type=bool, default=False, set to "True" to print out prediction 
'--print_truth',type=bool, default=False, set to "True" to print out ground truth 

4. helper.py 
Read and split the data. Running time for algorithm and error counts to measure the performance and implementation efficiency. 

5. main.py 
Connecting model.py, para_model.py, util.py and helper.py. 

Call main.py plus neccessary arguments in terminal to get predictions. 

Terminal Command Example:
python main.py --method Frequency --update_step 10 --pred_length 5
(use frequency method, start to predict after first 10 questions are answered, predcit next 5 question per iteration)

python main.py --method RF --train_flag True --update_step 5 --pred_length 10
(use RF to train model, this model will be store in a directory called "RFmodel")

python main.py --method CART --train_flag True --test_flag True --update_step 5 --pred_length 10
(use RF to train model and then make predictions, this model will be store in a directory called "CARTmodel". When making predictions, the model starts to predict after first 5 questions are answered, predcit next 10 question per iteration)

python main.py --method CART --train_flag False --test_flag True --update_step 15 --pred_length 10
(use pretrained CART model-- stored in "CARTmodel" folder-- to make predictions. The model starts to predict after first 15 questions are answered, predcit next 10 question per iteration)

6. slackbot.py : lay foundation for implementation in the real business applications. The chatbot makes use of slack API and creative a prototype for interative production configuration system. The users of the chat bot are not required to know how to prorgam. By simply typing and confirming, he or she can get the prediction and construction a configuration faster than the traditional way. 

User Manual:
start a new oder: 
@NessusQ start an order

confirm default selection shown on the user interface: 
@NessusQ confirm 

change the answer for a specific question (e.g. question 6: 
@NessusQ change 6
(then all the available choices for question 6 will be shown on the user interface)
@NessusQ choice 
(choose one of the choices and type here)
@NessusQ confirm 
(confirm selection)

save prediction:
@NessusQ save
(the predction will be saved as an json file in the current working directory)


