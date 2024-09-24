*** Settings ***
Library    RequestsLibrary
Suite Setup   Set Base URL

*** Variables ***
${BASE_URL}  http://localhost:8000
${USER_CONSUMPTION_URL}  ${BASE_URL}/consumption/user/
${ADMIN_AGGREGATE_URL}  ${BASE_URL}/consumption/admin/aggregate/
${ADMIN_USER_AGGREGATE_URL}  ${BASE_URL}/consumption/admin/aggregate/user/1/  # Example for user_id 1

*** Test Cases ***

# User Test Cases
Create New Consumption Record
    [Documentation]    Test creating a new consumption record
    ${response}=    Create Consumption    2024-01-01    50.5    kWh
    Should Be Equal As Strings    ${response.status_code}    201

View Consumption Records
    [Documentation]    Test viewing consumption records
    ${response}=    Get User Consumption
    Should Be Equal As Strings    ${response.status_code}    200

Update Consumption Record
    [Documentation]    Test updating a consumption record
    ${response}=    Create Consumption    2024-01-01    50.5    kWh
    ${consumption_id}=    Get Consumption ID
    Update Consumption    ${consumption_id}    60.0    kWh
    Should Be Equal As Strings    ${response.status_code}    200

Delete Consumption Record
    [Documentation]    Test deleting a consumption record
    ${response}=    Create Consumption    2024-01-01    50.5    kWh
    ${consumption_id}=    Get Consumption ID
    Delete Consumption    ${consumption_id}
    Should Be Equal As Strings    ${response.status_code}    204

# Admin Test Cases
Admin View All Users' Consumption
    [Documentation]    Test admin viewing all users' consumption records
    ${response}=    Get All Users Consumption
    Should Be Equal As Strings    ${response.status_code}    200

Admin Aggregate All Users' Consumption
    [Documentation]    Test admin aggregating consumption across all users
    ${response}=    Get Aggregate All Users Consumption
    Should Be Equal As Strings    ${response.status_code}    200

Admin Aggregate Specific User's Consumption
    [Documentation]    Test admin aggregating consumption for a specific user
    ${response}=    Get Aggregate User Consumption
    Should Be Equal As Strings    ${response.status_code}    200


*** Keywords ***

Set Base URL
    Create Session    consumption    ${BASE_URL}

# User Actions
Create Consumption
    [Arguments]    ${date}    ${consumption}    ${unit}
    ${data}=  Create Dictionary    date=${date}    consumption=${consumption}    unit=${unit}
    ${response}=    Post Request    consumption    ${USER_CONSUMPTION_URL}    json=${data}
    Log    ${response.text}
    [Return]    ${response}

Get User Consumption
    ${response}=    Get Request    consumption    ${USER_CONSUMPTION_URL}
    Log    ${response.text}
    [Return]    ${response}

Update Consumption
    [Arguments]    ${consumption_id}    ${new_consumption}    ${unit}
    ${data}=  Create Dictionary    consumption=${new_consumption}    unit=${unit}
    ${url}=  Set Variable    ${USER_CONSUMPTION_URL}${consumption_id}/
    ${response}=    Put Request    consumption    ${url}    json=${data}
    Log    ${response.text}
    [Return]    ${response}

Delete Consumption
    [Arguments]    ${consumption_id}
    ${url}=  Set Variable    ${USER_CONSUMPTION_URL}${consumption_id}/
    ${response}=    Delete Request    consumption    ${url}
    Log    ${response.text}
    [Return]    ${response}

# Admin Actions
Get All Users Consumption
    ${response}=    Get Request    consumption    ${USER_CONSUMPTION_URL}
    Log    ${response.text}
    [Return]    ${response}

Get Aggregate All Users Consumption
    ${response}=    Get Request    consumption    ${ADMIN_AGGREGATE_URL}
    Log    ${response.text}
    [Return]    ${response}

Get Aggregate User Consumption
    ${response}=    Get Request    consumption    ${ADMIN_USER_AGGREGATE_URL}
    Log    ${response.text}
    [Return]    ${response}

Get Consumption ID
    ${response}=    Get Request    consumption    ${USER_CONSUMPTION_URL}
    ${consumption_id}=    Set Variable    ${response.json()[0]['id']}
    [Return]    ${consumption_id}
