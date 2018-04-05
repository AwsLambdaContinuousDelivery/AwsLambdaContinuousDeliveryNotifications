# awslambdacontinuousdelivery.notifications
## Overview

### Purpose
This package enables users to add
notifications to their AWS CodePipelines.

### Packages
- `awslambdacontinuousdelivery.notifications`
- `awslambdacontinuousdelivery.notifications.sns`

### License
- see `LICENSE` file

### Requirements
- `troposphere`
- `awacs`

## Quick Start
### E-Mail Notifications if any `Action` Fails
In order to get e-mail notifications if any `Action` in a pipeline fails
you need to call two functions: `addFailureNotifications` and `getEmailTopic`:

```python
from awslambdacontinuousdelivery.notifications.sns import getEmailTopic
from awslambdacontinuousdelivery.notifications import getFailureNotifications
from troposphere import Template

pipeline = "examplePipelineName"
template = Template()
emailTopic = getEmailTopic("klaus.kinski@example.com")
rule = addFailureNotifications(template, pipeline, emailTopic)
# done and dusted
print(template.to_json())
```

