*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    DateTime
Library    String
Library    Collections
Library    Process
#Library       docx    WITH NAME    WordLib

*** Variables ***
${SCREENSHOT_DIR}    ${CURDIR}${/}../../outputs/Screenshots

*** Keywords ***
Setup Test Environment
    Set Suite Variable     ${SCREENSHOT_DIR}    ${CURDIR}${/}../../outputs/Screenshots
    ${exists}=    Run Keyword And Return Status    Directory Should Exist    ${SCREENSHOT_DIR}
    Run Keyword If    not ${exists}     Create Directory    ${SCREENSHOT_DIR}
    Log To Console    Screenshot directory set to: ${SCREENSHOT_DIR}
#    ${DOC_PATH}          ${CURDIR}${/}../../outputs/Test_Screenshots.docx

Teardown Test Environment
    Close All Browsers

#Capture Screenshots
#    ${files}=    List Files In Directory    ${SCREENSHOT_DIR}    pattern=*.png
#    Create File    ${DOC_PATH}
#    WordLib.Create Document    ${DOC_PATH}
#    FOR    ${file}    IN    @{files}
#        ${justname}=    Get File Name    ${file}
#        WordLib.Add Paragraph    Test Screenshot: ${justname}
#        WordLib.Add Picture       ${file}    width=6in
#        WordLib.Add Paragraph     ---
#    END
#    WordLib.Save Document
#    Log To Console    \n All screenshots saved to: ${DOC_PATH}

Capture Screenshots
    [Arguments]    ${name}=screenshot
#    ${ts}=    Get Time    result_format=%Y-%m-%d_%H-%M-%S
    ${timestamp}=    Get Time    result_format=%Y-%m-%d %H:%M:%S
    ${timestamp}=    Replace String    ${timestamp}    :    ${EMPTY}
    ${timestamp}=    Replace String    ${timestamp}    ' '    '_'
    ${filename}=    Set Variable    ${SCREENSHOT_DIR}${/}${name}_${timestamp}.png
    Capture Page Screenshot        ${filename}
    Log To Console    Screenshot saved to     ${filename}
    [Return]    ${filename}

#Below old code has many errors
#    [Arguments]    ${status}
#    # Replace spaces in test name with _ (failed in last run due to spaces in file name)
#    ${test_name}=    Replace String Using Regexp    ${TEST NAME}    \s+    _
#    # Safe timestamp: YYYYMMDD_HHMMSS
#    Log To Console    >>> TIMESTAMP=${timestamp}
#    ${timestamp}=    Get Time    result_format=%Y%m%d_%H%M%S
#    ${folder_path}=    Set Variable    ${EXECDIR}/../../outputs/Screenshots/${test_name}
#    Create Directory    ${folder_path}
#    ${file_path}=    Set Variable    ${folder_path}/${test_name}_${timestamp}_${status}.png
#    Capture Page Screenshot    ${file_path}
#    Log To Console    Screenshot saved:     ${file_path}