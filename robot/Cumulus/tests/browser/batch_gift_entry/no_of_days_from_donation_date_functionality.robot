*** Settings ***

Resource        robot/Cumulus/resources/NPSP.robot
Library           DateTime
Suite Setup      Run keywords
...             Open Test Browser
...             Setup Test Data
Suite Teardown  Delete Records and Close Browser

*** Test Cases ***

Match Based on Number of Days from Donation Date Functionality
    [Documentation]    The number of days from donation date field on the BGE wizard allows matching to be made by providing a margin of error on the Donation Date field for a record. If the gift created is within range of that date, gift is matched to the existing donation
    [tags]  stable
    Set Window Size    1024    768  
    Select App Launcher Tab   Batch Gift Entry
    # Click Link  &{batch}[Name]
    Click Link With Text    &{batch}[Name]
    Wait For Locator    bge.title    Batch Gift Entry
    Select Value From BGE DD    Donor Type    Account
    Populate Field By Placeholder    Search Accounts    &{account}[Name]
    Click Link    &{account}[Name]
    Click Link With Text    Review Donations
    Page Should Contain    &{opp}[Name]
    ${pay_no}    Get BGE Card Header    &{opp}[Name]
    Log To Console    ${pay_no}
    Click Button    title:Close this window
    Click Element With Locator    bge.field-input    Donation Amount
    Fill BGE Form
    ...                       Donation Amount=100
    Click Element With Locator    bge.field-input    Donation Date
    Click BGE Button    Today
    Click BGE Button       Save
    Verify Row Count    1
    Page Should Contain Link    ${pay_no}
    Click BGE Button       Process Batch
    Click Data Import Button    NPSP Data Import    button    Begin Data Import Process
    Wait For Batch To Complete    data_imports.status    Completed
    Click Button With Value   Close
    Wait Until Element Is Visible    text:All Gifts
    # Verify that the gift matched to existing opportunity and updated it to closed won status with gift date and payment is paid
    Go To Record Home    &{opp}[Id]
    Confirm Value    Amount    $100.00    Y 
    ${date} =     Get Current Date    result_format=%-m/%-d/%Y
    Confirm Value    Close Date    ${date}    Y 
    Confirm Value    Stage    Closed Won    Y 
    Select Tab    Related
    Load Related List    GAU Allocations
    Click Link    ${pay_no}
    ${pay}    Get Current Record ID
    Store Session Record      npe01__OppPayment__c  ${pay}
    Verify Expected Values    nonns    npe01__OppPayment__c    ${pay}
    ...    npe01__Payment_Amount__c=100.0
    ...    npe01__Payment_Date__c=${api_date}
    ...    npe01__Paid__c=True   

***Keywords***
Setup Test Data
    ${ns} =  Get NPSP Namespace Prefix
    Set Suite Variable    ${ns}
    &{batch} =       API Create DataImportBatch    
    ...    ${ns}Batch_Process_Size__c=50
    ...    ${ns}Donation_Date_Range__c=5.0    
    ...    ${ns}Batch_Description__c=Created via API    
    ...    ${ns}Donation_Matching_Behavior__c=Single Match or Create    
    ...    ${ns}Donation_Matching_Rule__c=${ns}donation_amount__c;${ns}donation_date__c    
    ...    ${ns}RequireTotalMatch__c=false    
    ...    ${ns}Run_Opportunity_Rollups_while_Processing__c=true   
    ...    ${ns}GiftBatch__c=true    
    ...    ${ns}Active_Fields__c=[{"label":"Donation Amount","name":"${ns}Donation_Amount__c","sObjectName":"Opportunity","defaultValue":null,"required":true,"hide":false,"sortOrder":0,"type":"number","options":null},{"label":"Donation Date","name":"${ns}Donation_Date__c","sObjectName":"Opportunity","defaultValue":null,"required":false,"hide":false,"sortOrder":1,"type":"date","options":null}] 
    
    Set Suite Variable    &{batch}
    &{account} =     API Create Organization Account
    Set Suite Variable    &{account}
    ${api_date} =     Get Current Date    result_format=%Y-%m-%d
    Set Suite Variable    ${api_date}
    ${opp_date} =     Get Current Date    result_format=%Y-%m-%d    increment=2 days
    &{opp} =     API Create Opportunity   &{account}[Id]    Donation  
    ...    StageName=Prospecting    
    ...    Amount=100    
    ...    CloseDate=${opp_date}    
    ...    npe01__Do_Not_Automatically_Create_Payment__c=false    
    ...    Name=&{account}[Name] Test 100 Donation      
    Set Suite Variable    &{opp}
    