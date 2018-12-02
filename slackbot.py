# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 21:03:01 2018

@author: huang
"""

import os
import time
import re
from slackclient import SlackClient

#创建一个SlackClient的实例,并获取之前export出来的SLACK_BOT_TOKEN
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
 
#在bot启动之后，会获得一个userId，先初始化
starterbot_id = None
 
#以下常量备用
RTM_READ_DELAY = 1    #RTM实时通讯，读完消息后，一秒延迟
EXAMPLE_COMMAND = "start an order"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"    # @xxx 使用到的正则表达式

def parse_bot_commands(slack_events):
    """
        解析来自Slack RTM API的事件列表以查找bot命令，
        如果找到了bot命令，则此函数返回一个命令和通道的元组，
        如果未找到，则此函数返回无。
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None
 
def parse_direct_mention(message_text):
    """
        在消息文本中查找直接提及（在开头提及）
        并返回提到的用户ID。如果没有直接提及，则返回None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # 所述第一组包含的用户名，该第二组包含其余消息
    print('matches.group(1)', matches.group(1))
    print('matches.group(2).strip()', matches.group(2).strip())
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)
 
class NessusQ:
    def __init__(self, method='CART'):
        self.method='CART'
        
        self.confirmed_step=0
        self.generated_step=0
        self.pred_length=5
        self.known={}
        self.prediction={}
        self.on_change=False
        self.on_change_question=0
        
    
    def restart(self):
        self.confirmed_step=0
        self.generated_step=0
        self.pred_length=5
        self.known={}
        self.prediction={}
    
    def predict(self):
        return None
        

        
    def handle_command(self,command, channel):
        """
            如果命令已知，则执行机器人命令
        """

        # 默认响应是用户的帮助文本
        default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)
        REPLY_REMINDER = "If you confirm the prediction is right, reply \'confirm\', if you need to make a change, reply \'change+ the question number you want to change \'"
        # 查找并执行给定的命令，填充响应
        response = None
        # 这是您开始执行更多命令的地方！
        if self.on_change:
            self.on_change=False
            self.prediction[self.on_change_question]=command       
            response = "wrong prediction corrected, now predictions are:"+\
            '\n'+REPLY_REMINDER
            slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
            )
            
        if command.startswith("start an order"):
            self.restart()
            response = "Have cleaned memory and started a new order, here are some initial prediction for the first {} columns".format(self.pred_length)+\
            "\n"+REPLY_REMINDER
            

        if command.startswith("confirm"):
            self.confirmed_step=self.generated_step
            self.prediction=self.predict()
            response = "current answers confirmed\n"+\
            "new prediction of the next {}:".format(self.pred_length)
            
        if command.startswith("change"):
            self.prediction={}
            change_question_id=re.match("[\d+]",command)
            self.on_change=True 
            self.on_change_question=change_question_id
            response="Here are some options to that question or you can type in the answer yourself"
            
        if command.startswith("save"):
            #A function to save the order
            response = "order saved"
        # 将响应发送回通道
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

if __name__ == "__main__":
 
    #使用rtm_connect方法，启动bot;一旦连接成功后，会调用web api方法 （auth.test）去找到bot的user ID
    #每个bot在当前的app内都有属于自己的user ID，存储这个user ID 会帮助程序理解是谁在一个会话里提到了他
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        
        Q=NessusQ()
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            #对于每个读取的事件，该parse_bot_commands()函数确定事件是否包含Bot的命令。如果是，那么command将包含一个值，
            #该handle_command()函数决定如何处理该命令
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                Q.handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")