*** Settings ***

Resource        robot/Cumulus/resources/NPSP.robot
Suite Setup     Open Test Browser
Suite Teardown  Delete Records and Close Browser

*** Variables ***
${level_name}
${contact_id}

*** Test Cases ***

1 Create Level and Verify Fields
    [tags]  unstable
    ${level_id}  ${level_name}     Create Level
    Set Global Variable      ${level_name}
    Set Global Variable      ${level_id}
    Go To Record Home        ${level_id}
    Confirm Value    Minimum Amount (>=)    0.10    Y
    Page Should Contain  0.9  # work around platform not showing the right number of decimals

2 Edit Level and Verify Fields
    # --------------------------------
    # Modify the Level Values and validate that they save correctly
    # --------------------------------
    [tags]  unstable
    Click Link    link=Show more actions
    Click Link    link=Edit
    Wait For Locator    frame    Levels
    Choose Frame    Levels
    Enter Level Dd Values    Source Field    Smallest Gift
    Enter Level Values
    ...            Minimum Amount=0.01
    ...            Maximum Amount=0.99
    Set Focus To Element   xpath: //input[@value='Save']
    Click Button  Save
    #adding a workaround to go back to levels tab due to core issue
    Unselect Frame
    Select App Launcher Tab  Levels
    Click Link    link=${level_name}
    # Wait For Locator  breadcrumb  Level
    # Reload Page
    Wait Until Loading Is Complete
    Confirm Value    Minimum Amount (>=)    0.01    Y
    Confirm Value    Maximum Amount (<)     0.99    Y
    Confirm Value    Source Field    npo02__SmallestAmount__c    Y

3 Validate Level Assignment in Batch Job
    [tags]  unstable
    # --------------------------------
    # Modify the SmallestGift field to allow the level to be applied
    # --------------------------------
    &{contact} =  API Create Contact
    Set Global Variable     ${contact_id}       &{contact}[Id]
    Go To Record Home       ${contact_id}
    Scroll Element Into View    text:Donation Totals
    Click Button       title:Edit Smallest Gift
    Wait For Locator  record.edit_form
    Populate Field          Smallest Gift     0.75
    Click Record Button     Save
    Wait Until Loading Is Complete
    Scroll Element Into View    text:Donation Totals
    Confirm Value           Smallest Gift    $0.75    Y
    # --------------------------------
    # Open NPSP Settings and run the Levels batch job
    # --------------------------------
    Open NPSP Settings      Bulk Data Processes         Level Assignment Batch
    Click Settings Button    idPanelLvlAssignBatch    Run Batch
    Wait for Locator        npsp_settings.completed
    # --------------------------------
    # Return to the Contact to validate the updated Level field
    # --------------------------------
    Go To Record Home       ${contact_id}
    Verify Field Value      Level    ${level_name}    Y
    # --------------------------------
    # Modify the SmallestGift field to change the applied level
    # --------------------------------
    Scroll Element Into View    text:Donation Totals
    Click Button       title:Edit Smallest Gift
    Wait For Locator  record.edit_form
    Populate Field          Smallest Gift     2.0
    Click Record Button     Save
    Wait Until Loading Is Complete
    Scroll Element Into View    text:Donation Totals
    Confirm Value           Smallest Gift    $2.00    Y
    # --------------------------------
    # Open NPSP Settings and run the Levels batch job
    # --------------------------------
    Open NPSP Settings      Bulk Data Processes         Level Assignment Batch
    Click Element With Locator    npsp_settings.batch-button    idPanelLvlAssignBatch    Run Batch
    Wait for Locator        npsp_settings.completed
    # --------------------------------
    # Return to the Contact to validate the updated Level field
    # --------------------------------
    Go To Record Home       ${contact_id}
    Confirm Value           Level               ${level_name}    N
    Verify Field Value      Previous Level      ${level_name}    Y

4 Delete Level and Validate Contact
    [tags]  unstable
    # --------------------------------
    # Delete the Level and validate that it was removed from the Contact
    # --------------------------------
    Click Link    link=${level_name}
    Click Link    link=Show more actions
    Click Link    link=Delete
    Click Modal Button    Delete
    Go To Record Home           ${contact_id}
    Confirm Value    Level      ${level_name}    N
