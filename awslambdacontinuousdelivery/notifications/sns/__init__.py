# By Janos Potecki
# University College London
# January 2018

from awacs.aws import Policy
from awacs.sns import Publish
from awslambdacontinuousdelivery.tools import alphanum

from troposphere import Sub, Template, Ref
from troposphere.sns import Subscription, Topic, TopicPolicy

from typing import List


def getTopic(name: str, subscriptions: List[Subscription], topicName: str = None) -> Topic:
    return Topic( "".join([alphanum(name), "SnsTopic"])
                , DisplayName = Sub("".join(["${AWS::StackName}", name, "SnsTopic"]))
                , Subscription = subscriptions
                , TopicName = Sub("".join(["${AWS::StackName}", name, "SnsTopic"]))
                )


def getEmailSubscription(emailAddr: str) -> Subscription:
    return Subscription( "EmailSubscription"
                       , Endpoint = emailAddr
                       , Protocol = "email"
                       )


def getEmailTopic(topicName: str, emailAddr: str) -> Topic:
    sub = getEmailSubscription(emailAddr)
    return getTopic(topicName, [sub], topicName)


def getTopicPolicy(topics: List[Topic]) -> TopicPolicy:
    topics = list(map(lambda x: Ref(x), topics))
    policyDoc = { "Version": "2008-10-17"
                , "Id": Sub("TopicsPublicationPolicy${AWS::StackName}")
                , "Statement":
                     [ { "Sid": "Allow-SNS-SendMessage"
                       , "Effect": "Allow"
                       , "Principal": { "AWS": "*" }
                       ,  "Action": [ Publish ]
                       ,  "Resource": "*"
                       }
                     ]
                }    
    return TopicPolicy( "TopicPolicy"
                      , Topics = topics
                      , PolicyDocument = policyDoc
                      )

