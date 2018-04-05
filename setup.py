#!/usr/bin/env python

from distutils.core import setup

setup( name='AwsLambdaContinuousDeliveryNotifications'
     , version = '0.0.1'
     , description = 'AwsLambdaContinuousDeliveryNotifications'
     , author = 'Janos Potecki'
     , url = 'https://github.com/AwsLambdaContinuousDelivery/AwsLambdaContinuousDeliveryNotifications'
     , packages = [ 'awslambdacontinuousdelivery.notifications'
                  , 'awslambdacontinuousdelivery.notifications.sns'
                  ]
     , license='MIT'
     , install_requires = [ 
          'troposphere'
        , 'awacs' 
        ]
     )
