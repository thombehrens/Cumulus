*** Settings ***

Resource        robot/Cumulus/resources/NPSP.robot
Library           DateTime
Suite Setup     Open Test Browser
Suite Teardown  Delete Records and Close Browser

*** Test Cases ***

Create a new opportunity for a contact with open donations
    #Enter an account with open donations, then clear it and enter a contact with open donations, then choose to create a new opp and process it
    [tags]  stable
    Set Window Size    1024    768
    ${ns} =  Get NPSP Namespace Prefix
    &{batch} =       API Create DataImportBatch    
    ...    ${ns}Batch_Process_Size__c=50    
    ...    ${ns}Batch_Description__c=Created via API    
    ...    ${ns}Donation_Matching_Behavior__c=Single Match or Create    
    ...    ${ns}Donation_Matching_Rule__c=${ns}donation_amount__c;${ns}donation_date__c    
    ...    ${ns}RequireTotalMatch__c=false    
    ...    ${ns}Run_Opportunity_Rollups_while_Processing__c=true   
    ...    ${ns}GiftBatch__c=true    
    ...    ${ns}Active_Fields__c=[{"label":"Donation Amount","name":"${ns}Donation_Amount__c","sObjectName":"Opportunity","defaultValue":null,"required":true,"hide":false,"sortOrder":0,"type":"number","options":null},{"label":"Donation Date","name":"${ns}Donation_Date__c","sObjectName":"Opportunity","defaultValue":null,"required":false,"hide":false,"sortOrder":1,"type":"date","options":null}] 
    &{account} =     API Create Organization Account
    &{contact} =     API Create Contact
    Store Session Record      Account    &{contact}[AccountId]
    ${date} =     Get Current Date    result_format=%Y-%m-%d
    &{opportunity1} =     API Create Opportunity   &{account}[Id]    Donation  StageName=Prospecting    Amount=100    CloseDate=${date}  
    &{opportunity2} =     API Create Opportunity   &{contact}[AccountId]    Donation  StageName=Prospecting    Amount=100    CloseDate=${date}      
    Select App Launcher Tab   Batch Gift Entry
    #Click Link  &{batch}[Name]
    Click Link With Text    &{batch}[Name]
    Wait For Locator    bge.title    Batch Gift Entry
    Select Value From BGE DD    Donor Type    Account
    Populate Field By Placeholder    Search Accounts    &{account}[Name]
    Click Link    &{account}[Name]
    Click Link With Text    Review Donations
    Click BGE Button    Update this Opportunity
    Select Value From BGE DD    Donor Type    Contact
    Page Should Not Contain Link    Review Donations
    Populate Field By Placeholder    Search Contacts    &{contact}[FirstName] &{contact}[LastName]
    Click Link    &{contact}[FirstName] &{contact}[LastName]
    Click Link With Text    Review Donations
    Click Link    Alternatively, create a new Opportunity.
    Fill BGE Form
    ...                       Donation Amount=20
    Click Field And Select Date    Donation Date    Today
    Click BGE Button       Save
    # Reload Page
    Verify Row Count    1
    Page Should Not Contain Link    &{opportunity2}[Name]
    Wait For Locator    bge.edit_button    Donation Amount
    Click BGE Edit Button    Donation Amount  
    Wait For Locator    bge.edit_field   
    Populate BGE Edit Field    Donation Amount    100
    Click Element With Locator    span    Donation Date
    Page Should Not Contain Link    &{opportunity2}[Name]
    Scroll Page To Location    0    0
    Click BGE Button       Process Batch
    # Select Frame With Title    NPSP Data Import
    # Click Button With Value   Begin Data Import Process
    Click Data Import Button    NPSP Data Import    button    Begin Data Import Process
    Wait For Batch To Complete    data_imports.status    Completed
    Click Button With Value   Close
    Wait Until Element Is Visible    text:All Gifts
    Verify Expected Values    nonns    Opportunity    &{opportunity2}[Id]
    ...    Amount=100.0
    ...    CloseDate=${date}
    ...    StageName=Prospecting 
    Sleep    2
    ${value}    Return Locator Value    bge.value    Donation
    #Click Link    text:${value}
    Click Link With Text    ${value}
    Select Window    ${value} | Salesforce    10
    ${opp_name}    Return Locator Value    check_field_spl    Opportunity
    Click Link    ${opp_name}
    ${newopp_id}    Get Current Record ID
    Store Session Record    Opportunity    ${newopp_id}
    Confirm Value    Amount    $100.00    Y 
    ${opp_date} =     Get Current Date    result_format=%-m/%-d/%Y
    Confirm Value    Close Date    ${opp_date}    Y 
    Confirm Value    Stage    Closed Won    Y 
    Go To Record Home    &{contact}[Id]
    Select Tab     Related
    Load Related List    Opportunities
    Verify Occurrence    Opportunities    2
      
