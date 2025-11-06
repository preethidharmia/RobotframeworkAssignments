*** Settings ***
Resource    ../pages/FormpageUI.robot
Resource    ../src/Utils/BrowserUtils.robot

*** Keywords ***
Fill And Verify Form
    Open Form Page
    Zoom And Scroll To Form
    Enter Student Details
    Submit Form
    Verify Submission successful
