*** Settings ***

Resource        robot/Cumulus/resources/NPSP.robot
Suite Setup     Run Keywords
...             Open Test Browser
...             Setup Variables
...             Setup Test Data
Suite Teardown  Delete Records and Close Browser

*** Keywords ***
Setup Variables
    ${ns} =                      Get NPSP Namespace Prefix
    Set Suite Variable           ${ns}

Setup Test Data
    #Create two Contacts in the Same Household
    &{primarycontact} =          API Create Contact             Email=jjoseph@robot.com
    Set Suite Variable           &{primarycontact}
    ${account_id} =              Set Variable                   &{primarycontact}[AccountId]
    Set Suite Variable           ${account_id}
    Store Session Record         Account                        ${account_id}
    &{householdcontact} =        API Create Contact             AccountId=${account_id}
    Set Suite Variable           ${householdcontact}

    #Create a Fixed Length Recurring Donation
    &{recurringdonation} =       API Create Recurring Donation  npe03__Contact__c=&{primarycontact}[Id]
    ...                          Name=Julian Recurring Donation
    ...                          npe03__Amount__c=10
    ...                          npe03__Installments__c=50
    ...                          npe03__Schedule_Type__c=Multiply By
    ...                          npe03__Installment_Period__c=Weekly
    Set Suite Variable           ${recurringdonation}

*** Test Cases ***

Create Fixed Length Recurring Donation Multiply By
    [Documentation]              This test verifies that Opportunities with the proper mulitplied amount are created for a Recurring Donation.
    ...                          This test case also verified the correct number of opportunities are created and related Account, Contact, 
    ...                          and Soft Credit Contact rollups are udpated.

    #Find 1st Opportunity for Recurring Donation and Close It
    @{opportunity1} =            API Query Installment         &{recurringdonation}[Id]    (1 of 50)
    Store Session Record         Opportunity                   ${opportunity1}[0][Id]
    Go To Record Home            ${opportunity1}[0][Id]
    Click Link                   link=Edit
    Click Dropdown               Stage
    Click Link                   link=Closed Won
    Click Modal Button           Save

    #Find 2nd Opportunity for Recurring Donation and Close It
    @{opportunity2} =            API Query Installment         &{recurringdonation}[Id]    (2 of 50)
    Store Session Record         Opportunity                   ${opportunity2}[0][Id]
    Go To Record Home            ${opportunity2}[0][Id]
    Click Link                   link=Edit
    Click Dropdown               Stage
    Click Link                   link=Closed Won
    Click Modal Button           Save
    

    #Open NPSP Settings and run Rollups Donations Batch job
    Run Donations Batch Process

    #Check if 50th Opportunity for Recurring Donation Exists
    @{opportunity50} =           API Query Installment          &{recurringdonation}[Id]    (50 of 50)
    Go To Record Home            ${opportunity50}[0][Id]

    #Check Rollups on Recurring Donation
    Go To Record Home            &{recurringdonation}[Id]
    Confirm Value                Number Of Paid Installments    2         Y
    Confirm Value                Total Paid Amount              $20.00    Y

    #Check Soft Credit Rollups on Household Contact
    Go To Record Home            &{householdcontact}[Id]
    Select Tab                   Details
    Scroll Element Into View     text:Household Donation Info
    Confirm Value                Soft Credit Total              $20.00    Y
    Confirm Value                Number of Soft Credits         2         Y

    #Check Rollups on Recurring Account
    Go To Record Home            ${account_id}
    Select Tab                   Details
    Scroll Element Into View     text:Membership Information
    Confirm Value                Total Gifts                    $20.00    Y
    Confirm Value                Total Number of Gifts          2         Y