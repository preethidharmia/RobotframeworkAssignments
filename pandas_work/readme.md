Error / Issues:
(venv) PS C:\Users\hp\PycharmProjects\Robotic_Framework_Assignments\tests> robot csv2ui2xl.robot
==============================================================================
Csv2Ui2Xl :: Multi-user login verification (positive + negative) using pand...
==============================================================================
Positive Login Tests :: One test per user with correct password ->... 
DevTools listening on ws://127.0.0.1:50761/devtools/browser/1193e28b-21b0-4c61-a3aa-7d4aa7863ad9
..
=== Test 1: standard_user / secret_sauce (expect success) ===

=== Test 2: locked_out_user / secret_sauce (expect success) ===
Positive Login Tests :: One test per user with correct password ->... | FAIL |
Element with locator 'id=user-name' not found.
------------------------------------------------------------------------------
Negative Login Tests :: One test per user with correct password ->... 
DevTools listening on ws://127.0.0.1:59658/devtools/browser/a15c1960-4a43-4778-93c5-ea2038f36da5
..
=== Test 3: standard_user / wrong_password (expect fail) ===

=== Test 4: locked_out_user / wrong_password (expect fail) ===

=== Test 5: problem_user / wrong_password (expect fail) ===

=== Test 6: performance_glitch_user / wrong_password (expect fail) ===
Negative Login Tests :: One test per user with correct password ->... | PASS |
------------------------------------------------------------------------------

Excel: C:\Users\hp\PycharmProjects\Robotic_Framework_Assignments\tests/../outputs/results.xlsx

Word: C:\Users\hp\PycharmProjects\Robotic_Framework_Assignments\tests/../outputs/evidence.docx
Csv2Ui2Xl :: Multi-user login verification (positive + negative) u... | FAIL |
2 tests, 1 passed, 1 failed
==============================================================================
Output:  C:\Users\hp\PycharmProjects\Robotic_Framework_Assignments\tests\output.xml
Log:     C:\Users\hp\PycharmProjects\Robotic_Framework_Assignments\tests\log.html
Report:  C:\Users\hp\PycharmProjects\Robotic_Framework_Assignments\tests\report.html
