*** Settings ***
Documentation     Smart multi-user login verification with expected outcomes.
...               Handles success AND locked-out scenarios.

Library           SeleniumLibrary
Library           CSVLibrary

*** Variables ***
${URL}            https://www.saucedemo.com/
${CSV_FILE}       ../data/logindetails.csv
${TIMEOUT}        10s
${BROWSER}        chrome

*** Test Cases ***
Multi User Login Verification
    [Documentation]    Read CSV, skip header, login each user, validate inventory

    # Read CSV → returns list of lists
    ${all_rows}=    Read Csv File To List    ${CSV_FILE}

    # Skip first row (header): username,password
    ${users}=       Set Variable    ${all_rows}[1:]

    # Loop through each user
    FOR    ${row}    IN    @{users}
        ${username}=    Set Variable    ${row}[0]
        ${password}=    Set Variable    ${row}[1]

        Open Browser    ${URL}    ${BROWSER}
        Maximize Browser Window
        Set Selenium Timeout    ${TIMEOUT}

        Log To Console    \n=== Testing: ${username} ===

        Input Text      id=user-name      ${username}
        Input Text      id=password      ${password}
        Click Element   id=login-button

        # === Smart Validation Based on Username ===
        Run Keyword If    '${username}' == 'locked_out_user'
        ...    Validate Locked Out User
        ...  ELSE
        ...    Validate Successful Login    ${username}

        Close Browser
    END

    Log To Console    \nALL USERS VERIFIED SUCCESSFULLY!

*** Keywords ***
Validate Successful Login
    [Arguments]    ${username}
    Wait Until Page Contains    Products              ${TIMEOUT}
    Wait Until Element Is Visible   css:.inventory_list    ${TIMEOUT}
    Log To Console    SUCCESS: ${username} → Logged in
    Log To Console    SUCCESS: ${username} → Inventory page loaded
    Capture Page Screenshot    ../outputs/Screenshots/success_${username}.png

Validate Locked Out User
    Wait Until Element Is Visible    css=[data-test="error"]    ${TIMEOUT}
    ${error}=    Get Text    css=[data-test="error"]
    Should Contain    ${error}    locked out
    Log To Console    EXPECTED FAILURE: locked_out_user → Error shown
    Capture Page Screenshot    ../outputs/Screenshots/error_locked_out.png