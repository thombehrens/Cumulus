*** Settings ***

Resource        robot/Cumulus/resources/NPSP.robot
Suite Setup     Open Test Browser
Suite Teardown  Delete Records and Close Browser

*** Test Cases ***

BGE Batch With Default Values
    #Create a BGE batch with default values
    [tags]  stable
    Set Window Size    1024    768
    ${batch} =           Generate Random String
    Select App Launcher Tab   Batch Gift Entry
    Click BGE Button       New Batch
    Fill BGE Form
    ...                       Name=${batch}
    ...                       Batch Description=This batch is created by Robot
    Click BGE Button        Next
    Click BGE Button        Next
    Click BGE Button        Next
    Click BGE Button        Save
    Wait For Locator    bge.title    Batch Gift Entry
    Verify Title    Batch Gift Entry    ${batch}
    ${batch_id}    Get Current Record Id
    ${ns} =  Get NPSP Namespace Prefix
    Store Session Record      ${ns}DataImportBatch__c  ${batch_id}
    Verify Expected Batch Values    ${batch_id}
    ...    Batch_Process_Size__c=50.0
    ...    Donation_Date_Range__c=0.0
    ...    Donation_Matching_Behavior__c=Single Match or Create
    ...    Donation_Matching_Implementing_Class__c=None
    ...    Donation_Matching_Rule__c=${ns}donation_amount__c;${ns}donation_date__c
    ...    Expected_Count_of_Gifts__c=0.0
    ...    Expected_Total_Batch_Amount__c=0.0
    ...    Post_Process_Implementing_Class__c=None
    ...    RequireTotalMatch__c=False
    ...    Run_Opportunity_Rollups_while_Processing__c=True
Create New gift and process batch and validate
    [tags]  stable
    &{contact} =     API Create Contact
    Select Value From BGE DD    Donor Type    Contact
    Populate Field By Placeholder    Search Contacts    &{contact}[FirstName] &{contact}[LastName]
    Click Link    &{contact}[FirstName] &{contact}[LastName]
    Fill BGE Form    Donation Amount=100
    Click Field And Select Date    Donation Date    Today
    Click BGE Button       Save
    Click BGE Button       Process Batch
    Click Data Import Button    NPSP Data Import    button    Begin Data Import Process
    Wait For Batch To Complete    data_imports.status    Completed
    Click Button With Value   Close
    Wait Until Element Is Visible    text:All Gifts
    Verify Row Count    1
    Page Should Contain    PMT-
    
             