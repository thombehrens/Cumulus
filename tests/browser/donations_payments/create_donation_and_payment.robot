*** Settings ***

Resource        tests/NPSP.robot
Suite Setup     Open Test Browser
Suite Teardown  Delete Records and Close Browser

*** Variables ***
${No_of_payments}     5
${intervel}    2
${frequency}    Month
${opp_name}

*** Test Cases ***

Create Donation from a Contact
    [tags]  unstable
    &{contact} =  API Create Contact    Email=skristem@robot.com
    &{opportunity} =  API Create Opportunity    &{Contact}[AccountId]    Donation    Name=Sravani $100 donation
    Go To Record Home  &{opportunity}[Id]
    ${opp_name}    Get Main Header 
    Set Global Variable      ${opp_name}
    Load Related List    Payments
    Select Related Dropdown    Payments
    Wait For Locator    link-title    Schedule Payments
    Click Link    link=Schedule Payments
    Wait For Locator    frame    Create one or more Payments for this Opportunity
    Select Frame with Title    Create one or more Payments for this Opportunity
    Enter Payment Schedule    ${No_of_payments}    ${intervel}    ${frequency}
    ${loc}    Get NPSP Locator    id    inputX
    Input Text    ${loc}    8/15/2018
    Click Button With Value    Calculate Payments
    ${value}     Verify Payment Split   100    ${No_of_payments}
    Should be equal as strings    ${value}    ${No_of_payments}
    Verify Date Split    8/15/2018    ${No_of_payments}    ${intervel}
    Click Button with Value    Create Payments
    ${value}    Verify Occurrence Payments    Payments
    Should not be equal as strings    ${value}    0
    
Verify Payments 
    [tags]  unstable
    Go To Object Home         Opportunity
    Click Link    ${opp_name}  
    Click ViewAll Related List    Payments
    Reload Page
    ${flag}     Verify payment    
    should be equal as strings     ${flag}    pass
