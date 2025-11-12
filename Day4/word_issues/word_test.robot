*** Settings ***
Library    WordHelper.py

*** Variables ***
${OUTPUT_DOC}    ${CURDIR}/../outputs/test_word_output.docx
${IMG_PATH}      ${CURDIR}/../data/Pictures/clouds_mountain.png

*** Test Cases ***
Verify Word Document Creation
    Create Doc    ${OUTPUT_DOC}
    Add Paragraph    Hi \nHow are you?
    Add Picture      ${IMG_PATH}    10
    Add Paragraph    This is after the image
    Save And Close
