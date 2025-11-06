*** Settings ***
Library    SeleniumLibrary
Resource   ../data/testdata.robot

*** Keywords ***
Open Form Page
    Open Browser    ${URL}    ${BROWSER}    options=${CHROME OPTIONS}
    Maximize Browser Window
    Zoom And Scroll To Form    0.67
    Set Selenium Speed    0.0
    Sleep    2s

Zoom And Scroll To Form
    [Arguments]    ${zoom}=0.67
    Execute JavaScript    document.body.style.zoom='${zoom}'
    Sleep    1s
    Execute JavaScript    document.getElementById('userForm').scrollIntoView({behavior: "smooth", block: "center"})
    Sleep    1s
    Wait Until Element Is Visible    id=submit

Enter Student Details
    Input Text    id:firstName    ${FIRSTNAME}
    Input Text    id:lastName     ${LASTNAME}
    Input Text    id:userEmail    ${EMAIL}

#    Wait Until Element Is Visible    xpath=//div[@id="subjectsContainer"]//input    10s
#    Scroll Element Into View    xpath=//div[@id="subjectsContainer"]//input
#    Sleep    1s
    Click Element    xpath=//label[normalize-space(text())='${GENDER}']

#    Click Element    xpath=//label[text()='${GENDER}']
#    ${gender_elem}=    Get WebElement    xpath=//label[normalize-space(text())='${GENDER}']
#    ${gender_list}=    Create List    ${gender_elem}

    Input Text    id:userNumber    ${MOBILE}

#    Wait Until Element Is Visible    xpath=//div[@id="subjectsContainer"]//input    10s
#    Scroll Element Into View    xpath=//div[@id="subjectsContainer"]//input
#    Sleep    1s

    Click Element    id=dateOfBirthInput
    Select From List By Label    class=react-datepicker__month-select        October
    Select From List By Label    class=react-datepicker__year-select         2002
    Click Element    xpath=//div[@class='react-datepicker__day react-datepicker__day--024']

#    Wait Until Element Is Visible    xpath=//label[text()="currentAddress-label"]    1s
#    Scroll Element Into View    xpath=//label[text()="currentAddress-label"]
#    Sleep    1s

#    Click Element               xpath=//input[id="subjectsInput"]
#    Press Keys                  xpath=//input[id="subjectsInput"]    ${SUBJECT}
#    Press Keys                  xpath=//input[id="subjectsInput"]      ENTER

    Click Element        id=subjectsInput
    Press Keys            id=subjectsInput     ${SUBJECT}
    Press Keys            id=subjectsInput      ENTER

#    Click Element    xpath=//label[text()="currentAddress-label"]
#    ${hobby_elem}=    Get WebElement    xpath=//label[normalize-space(text())='${HOBBY}']
#    ${hobby_list}=    Create List    ${hobby_elem}

#    Scroll Element Into View    xpath=//input[@id='Hobbies']
#    Sleep    1s
    Click Element    xpath=//label[text()='${HOBBY}']

    Choose File    id:uploadPicture    ${UPLOAD_PIC}

    Input Text    id:currentAddress    ${ADDRESS}

    Click Element    id:state
    Click Element    xpath=//div[text()='${STATE}']

    Click Element    id:city
    Click Element    xpath=//div[text()='${CITY}']

Submit Form
    Scroll Element Into View    xpath=//button[@id='submit']
    Sleep    1s
    Click Button                xpath=//button[@id='submit']

Verify Submission successful
    Wait Until Element Is Visible    xpath=//div[@id='example-modal-sizes-title-lg']    15s
    Element Text Should Be           xpath=//div[@id='example-modal-sizes-title-lg']    ${SUCCESS_MESSAGE}
