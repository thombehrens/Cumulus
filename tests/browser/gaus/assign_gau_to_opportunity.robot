*** Settings ***

Resource        tests/NPSP.robot
Suite Setup     Open Test Browser
Suite Teardown  Delete Records and Close Browser

*** Test Cases ***

Assign GAU to Opportunity
    [tags]  unstable
    &{gau1} =  API Create GAU
    &{gau2} =  API Create GAU
    &{contact} =  API Create Contact    Email=skristem@robot.com
    &{opportunity} =  API Create Opportunity    &{Contact}[AccountId]    Donation    Name=Test GAU donation
    Go To Record Home  &{opportunity}[Id]
    Load Related List    GAU Allocations
    Select Related Dropdown    GAU Allocations
    Wait For Locator    link-title    Manage Allocations
    Click Link    link=Manage Allocations
    Wait For Locator    frame    Manage Allocations
    #Sleep    2
    Select Frame With Title    Manage Allocations
    Select Search    General Accounting Unit 0    &{gau1}[Name]
    Add GAU Allocation    Percent 0    50
    Click Button With Value    Add Row    
    Select Search    General Accounting Unit 1    &{gau2}[Name] 
    #sleep    2   
    Add GAU Allocation    Amount 1    20
    Click Save    GAU
    Verify Occurrence    GAU Allocations    2
   