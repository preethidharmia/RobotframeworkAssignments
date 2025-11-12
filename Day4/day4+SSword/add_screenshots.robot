*** Settings ***
Documentation       Smart multi-user login verification with expected outcomes.
...                 Handles success AND locked-out scenarios.

Library             SeleniumLibrary
Library             OperatingSystem
Library             CSVLibrary
Library             WordLibrary.py

*** Variables ***
${URL}              https://www.saucedemo.com/
${CSV_FILE}         ../data/logindetails.csv
${TIMEOUT}          10s
${BROWSER}          chrome
${REPORT_PATH}      ../outputs/report.docx
${SCREENSHOT_DIR}   ../outputs/Screenshots

*** Test Cases ***
Multi User Login Verification
    [Documentation]    Read CSV, login each user, capture screenshot, add to Word report.

    # Create output directories
    Create Directory    ${SCREENSHOT_DIR}

    # === Initialize Word Report ===
    Create Word Document        ${REPORT_PATH}
    Add Heading                 Multi-User Login Test Report    1
    Add Paragraph               This report shows login results for multiple users.
    Add Paragraph               --------------

    # === Read CSV Data ===
    ${all_rows}=                Read Csv File To List    ${CSV_FILE}
    ${users}=                   Set Variable    ${all_rows}[1:]

    # === Loop Through Users ===
    FOR    ${row}    IN    @{users}
        ${username}=            Set Variable    ${row}[0]
        ${password}=            Set Variable    ${row}[1]

        Open Browser            ${URL}    ${BROWSER}
        Maximize Browser Window
        Set Selenium Timeout    ${TIMEOUT}

        Log To Console          \n=== Testing User: ${username} ===

        Input Text              id=user-name    ${username}
        Input Text              id=password     ${password}
        Click Element           id=login-button

        Run Keyword If          '${username}' == 'locked_out_user'
        ...                     Validate Locked Out User    ${username}
        ...    ELSE
        ...                     Validate Successful Login   ${username}

        Close Browser
    END

    # === Finalize Report ===
    Add Paragraph               --------------
    Add Text                    All tests completed successfully.    bold=${False}    align=center
    Save Document

    Log To Console              \nWord report generated: ${REPORT_PATH}

*** Keywords ***
Validate Successful Login
    [Arguments]    ${username}

    Wait Until Page Contains        Products    ${TIMEOUT}
    Wait Until Element Is Visible   css:.inventory_list    ${TIMEOUT}

    Log To Console                  SUCCESS: ${username} logged in

    ${screenshot}=    Set Variable    ${SCREENSHOT_DIR}/success_${username}.png
    Capture Page Screenshot         ${screenshot}

    Add Heading                     Login Success: ${username}    2
    Add Text                        User successfully logged in and reached inventory page.    italic=${True}
    Add Image With Caption          ${screenshot}    Success: Inventory page for ${username}
    Add Paragraph                    --------------

Validate Locked Out User
    [Arguments]    ${username}

    Wait Until Element Is Visible   css=[data-test="error"]    ${TIMEOUT}
    ${error_msg}=    Get Text       css=[data-test="error"]
    Should Contain                  ${error_msg}    locked out

    Log To Console                  EXPECTED: ${username} is locked out

    ${screenshot}=    Set Variable    ${SCREENSHOT_DIR}/error_locked_out.png
    Capture Page Screenshot         ${screenshot}

    Add Heading                     Login Failed (Expected): ${username}    2
    Add Text                        User is locked out as expected.    italic=${True}
    Add Image With Caption          ${screenshot}    Error: Locked out for ${username}
    Add Paragraph                   --------------