# By Janos Potecki
# University College London
# January 2018

from awslambdacontinuousdelivery.tools import alphanum
from awslambdacontinuousdelivery.notifications.sns import getTopicPolicy

from troposphere import Template, Sub, Ref, Join
from troposphere.sns import Topic
from troposphere.events import Rule, Target, InputTransformer

from enum import Enum 
from typing import List

class PipelineState(Enum):
    def __str__(self):
        return self.value

    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    RESUMED = "RESUMED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    SUPERSEDED = "SUPERSEDED"

class StageState(Enum):
    def __str__(self):
        return self.value

    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    RESUMED = "RESUMED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"

class ActionState(Enum):
    def __str__(self):
        return self.value
    
    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


def addFailureNotifications( t: Template
                           , pipeName: str
                           , topic: Topic
                           , createTopicPolicy = True
                           ) -> Rule:
    '''
    Add notifications if any `Action` in the pipeline returns `FAILED`.

    Returns the `Rule` which has already been added to the `Template`

    Arguments:
    - `t: troposphere.Template` the template where the notifications should be added
    - `pipeName: str` String with the name of the pipeline for which the notifications should be added
    - `topic: troposphere.sns.Topic` The SNS topic to publish the notifications
    - Optional: `createTopicPolicy: bool` default: `True` adds the necessary `troposphere.sns.TopicPolicy` to the template to get permission to publish to the SNS topic.

    Before calling this function the user must create a `troposphere.sns.Topic` on which the notifications should be published.
    '''
    if topicPolicy:
        topicPolicy = getTopicPolicy([topic])
        template.add_resource(topicPolicy)
    topic_ = t.add_resource(topic)
    transformer = InputTransformer(
          InputPathsMap = { "pipeline" : "$.detail.pipeline" }
        , InputTemplate = '"Pipeline <pipeline> failed."'
    )
    target = Target( "FailureNotificationsTarget"
                   , Arn = Ref(topic_)
                   , Id = Join("-", [pipeName, "FailureNotificationsTarget"])
                   , InputTransformer = transformer
                   )
    rule = Rule( "FailureNotificationRule"
               , Description = Sub("Notification Rule for ${AWS::StackName}")
               , EventPattern = { "detail-type" :
                                  ["CodePipeline Action Execution State Change"]
                                , "source" : [ "aws.codepipeline" ]
                                , "detail" :
                                  { "state" :[ str(StageState.FAILED) ]
                                  }
                                }
               , Targets = [ target ]
               , State = "ENABLED"
               )
    return t.add_resource(rule)
