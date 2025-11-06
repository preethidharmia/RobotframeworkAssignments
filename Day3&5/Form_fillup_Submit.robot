*** Settings ***
Resource    ../config/reference.robot
Resource          ../src/Utils/BrowserUtils.robot
Suite Setup       Setup Test Environment
Suite Teardown    Teardown Test Environment
Test Setup        Log To Console    Starting test:     ${TEST NAME}
Test Teardown     Capture Screenshots    ${TEST STATUS}

*** Test Cases ***
Submit Student Registration Form
    Fill And Verify Form