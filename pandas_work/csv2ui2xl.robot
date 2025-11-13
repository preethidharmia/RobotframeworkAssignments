*** Settings ***
Documentation     Multi-user login verification (positive + negative) using pandas.
...               Results are written to Excel and screenshots to Word report.
Library            SeleniumLibrary
Library            OperatingSystem
Library            Collections
Library            WordLibrary.py    WITH NAME    WordLib
Library           ${CURDIR}/PandasLibrary.py    WITH NAME    PandasLib   # custom pandas wrapper (see below)

Suite Setup       Suite Setup Actions
Suite Teardown    Suite Teardown Actions
Test Setup        Test Setup Actions
Test Teardown     Test Teardown Actions

*** Variables ***
${URL}               https://www.saucedemo.com/
${TIMEOUT}           12s
${BROWSER}           chrome
${CSV_FILE}          ${CURDIR}/../data/users.csv
${SCREENSHOT_DIR}    ${CURDIR}/../outputs/Screenshots
${REPORT_PATH}       ${CURDIR}/../outputs/evidence.docx
${EXCEL_FILE}        ${CURDIR}/../outputs/results.xlsx


@{ALL_RESULTS}
${WORD}              ${NONE}    # Will hold WordLib instance
${TEST_NO}           0          # auto-increments the test-case

*** Test Cases ***
# ------------------------------------------------------------------
# Positive testcase
# ------------------------------------------------------------------
Positive Login Tests
    [Documentation]  One test per user with correct password -> expected PASS
    [Tags]    positive
    ${users}=    PandasLib.Read CSV With Pandas    ${CSV_FILE}

    FOR    ${user}    IN    @{users}
        ${TEST_NO}=    Evaluate    ${TEST_NO} + 1
        Set Suite Variable    ${TEST_NO}
        Run Keyword    Login And Verify
        ...    ${user['username']}    ${user['password']}    expected=success
    END

# ------------------------------------------------------------------
# Negative testcase
# ------------------------------------------------------------------
Negative Login Tests
    [Documentation]  One test per user with correct password -> expected FAIL
    [Tags]    negative
    ${users}=    PandasLib.Read CSV With Pandas    ${CSV_FILE}

    FOR    ${user}    IN    @{users}
        ${TEST_NO}=    Evaluate    ${TEST_NO} + 1
        Set Suite Variable    ${TEST_NO}
        Run Keyword    Login And Verify
        ...    ${user['username']}    wrong_password    expected=fail
    END

*** Keywords ***
# ------------------------------------------------------------------
# Suite setup and teardowns
# ------------------------------------------------------------------
Suite Setup Actions
    Create Directory    ${SCREENSHOT_DIR}
    ${word}=    WordLib.Create Word Document    ${REPORT_PATH}
    WordLib.Add Heading    Multi-User Login Test Report    1
    WordLib.Add Paragraph    This report contains screenshots for every execution.
    WordLib.Add Paragraph    --------------

Suite Teardown Actions
    PandasLib.Write Results To Excel    ${EXCEL_FILE}    ${ALL_RESULTS}
    Log To Console    \nExcel: ${EXCEL_FILE}
    Run Keyword If    '${WORD}' != '${NONE}'    WordLib.Add Paragraph    --------------
    Run Keyword If    '${WORD}' != '${NONE}'    WordLib.Add Text    All tests completed.    bold=${True}    align=center
    Run Keyword If    '${WORD}' != '${NONE}'    WordLib.Save Document
    Log To Console    \nWord: ${REPORT_PATH}

# ------------------------------------------------------------------
# Test setup and teardowns
# ------------------------------------------------------------------
Test Setup Actions
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}

Test Teardown Actions
    Close Browser

# ------------------------------------------------------------------
# keyword Login And Verify
# ------------------------------------------------------------------
Login And Verify
    [Arguments]    ${username}    ${password}    ${expected}
    Log To Console    \n=== Test ${TEST_NO}: ${username} / ${password} (expect ${expected}) ===

    Input Text         id=user-name      ${username}
    Input Text         id=password       ${password}
    Click Element      id=login-button

    ${screenshot}=    Set Variable    ${SCREENSHOT_DIR}/${TEST_NO}_${username}.png
    Capture Page Screenshot    ${screenshot}

    ${result}=    Run Keyword And Continue On Failure    Run Login Check    ${expected}

    # ------------------------------------------------------------------
    # Excel configuration
    # ------------------------------------------------------------------
    ${row}=    Create Dictionary
    ...    TestCaseNo=${TEST_NO}
    ...    UserName=${username}
    ...    Password=${password}
    ...    Result=${result}
    Append To List    ${ALL_RESULTS}    ${row}

    # ------------------------------------------------------------------
    # Word configuration
    # ------------------------------------------------------------------

    Run Keyword If    '${WORD}' != '${NONE}'
    ...    WordLib.Add Heading    Test ${TEST_NO}: ${username}    2

    Run Keyword If    '${WORD}' != '${NONE}'
    ...    WordLib.Add Text    Expected: ${expected} – Result: ${result}    italic=${True}

    Run Keyword If    '${WORD}' != '${NONE}'
    ...    WordLib.Add Image With Caption    ${screenshot}
    ...    ${result}: ${username} (pwd: ${password})

    Run Keyword If    '${WORD}' != '${NONE}'    WordLib.Add Paragraph       --------------

# ------------------------------------------------------------------
# logic part to determine pass or failure scenario
# ------------------------------------------------------------------

Run Login Check
    [Arguments]    ${expected}
    ${result}=    Set Variable    FAIL
    IF    '${expected}' == 'success'
        ${status}    ${value}=    Run Keyword And Ignore Error
        ...    Wait Until Page Contains    Products    ${TIMEOUT}
        ${result}=    Set Variable If    '${status}' == 'PASS'    PASS    FAIL
    ELSE
        ${status}    ${value}=    Run Keyword And Ignore Error
        ...    Wait Until Element Is Visible    css=[data-test="error"]    ${TIMEOUT}
        ${error}=    Run Keyword If    '${status}' == 'PASS'    Get Text    css=[data-test="error"]
        ${result}=    Set Variable If    '${status}' == 'PASS' and 'Epic sadface' in '''${error}'''    PASS    FAIL
    END
    [Return]    ${result}