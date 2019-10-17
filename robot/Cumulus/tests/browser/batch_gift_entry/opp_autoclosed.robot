*** Settings ***

Resource        robot/Cumulus/resources/NPSP.robot
Library           DateTime
Suite Setup     Open Test Browser
Suite Teardown  Delete Records and Close Browser

*** Test Cases ***

Opportunity is Autoclosed when Overpaid
    [Documentation]    Create Open Opportunity and apply new payment of amount more than opportunity amount and confirm that opportunity is closed when batch is processed
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
    &{contact} =     API Create Contact
    Store Session Record      Account    &{contact}[AccountId] 
    ${date} =     Get Current Date    result_format=%Y-%m-%d
    &{opportunity} =     API Create Opportunity   &{contact}[AccountId]    Donation  
    ...    StageName=Prospecting    
    ...    Amount=100    
    ...    CloseDate=${date}
    ...    Name=&{contact}[LastName] Test Donation    
    Select App Launcher Tab   Batch Gift Entry
    # Click Link  &{batch}[Name]
    Click Link With Text    &{batch}[Name]
    Wait For Locator    bge.title    Batch Gift Entry
    Populate Field By Placeholder    Search Contacts    &{contact}[FirstName] &{contact}[LastName]
    Click Link    &{contact}[FirstName] &{contact}[LastName]
    Click Link With Text    Review Donations
    Click BGE Button    Apply New Payment
    Page Should Contain     You are currently applying a new Payment to Opportunity:&{opportunity}[Name]
    Fill BGE Form
    ...                       Donation Amount=101
    Click Field And Select Date    Donation Date    Today
    Click BGE Button       Save
    Verify Row Count    1
    Page Should Contain Link    &{opportunity}[Name]
    Click BGE Button       Process Batch
    Click Data Import Button    NPSP Data Import    button    Begin Data Import Process
    Wait For Batch To Complete    data_imports.status    Completed
    Click Button With Value   Close
    Wait Until Element Is Visible    text:All Gifts
    ${value}    Return Locator Value    bge.value    Donation
    # Click Link    ${value}
    Click Link With Text    ${value}
    Select Window    ${value} | Salesforce    10
    ${pay_id}    Get Current Record ID
    Store Session Record      npe01__OppPayment__c  ${pay_id}
    Verify Expected Values    nonns    npe01__OppPayment__c    ${pay_id}
    ...    npe01__Payment_Amount__c=101.0
    ...    npe01__Payment_Date__c=${date}
    ...    npe01__Paid__c=True
    Go To Record Home    &{opportunity}[Id]
    Confirm Value    Amount    $100.00    Y 
    ${opp_date} =     Get Current Date    result_format=%-m/%-d/%Y
    Confirm Value    Close Date    ${opp_date}    Y 
    Confirm Value    Stage    Closed Won    Y 
    
