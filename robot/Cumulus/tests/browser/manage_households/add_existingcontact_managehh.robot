*** Settings ***

Resource        robot/Cumulus/resources/NPSP.robot
Suite Setup     Open Test Browser
Suite Teardown  Capture Screenshot and Delete Records and Close Browser

*** Test Cases ***

Add Existing Contact to Existing Household through Manage Household Page
    [tags]  unstable
    &{contact1} =  API Create Contact    Email=skristem@robot.com
    Store Session Record    Account    &{contact1}[AccountId]   
    &{contact2} =  API Create Contact
    Store Session Record    Account    &{contact2}[AccountId]
    Go To Record Home  &{contact2}[AccountId] 
    # Click Link    link=Show more actions
    Click Link    link=Manage Household    
    Sleep     5
    Choose Frame   Manage Household
    Populate Field By Placeholder    Find a Contact or add a new Contact to the Household    &{contact1}[FirstName] &{contact1}[LastName]
    Click Button  title=Add
    Sleep  5
    Click Button       title=Save
    Unselect Frame
    Wait Until Url Contains    /view
    Wait Until Page Contains    Account Owner
    Wait For Record To Update    &{contact2}[AccountId]    &{contact2}[LastName] and &{contact1}[LastName] Household
    Select Tab    Related
    Load Related List    Contacts
    Verify Related List Items    Contacts    &{contact1}[FirstName] &{contact1}[LastName]
