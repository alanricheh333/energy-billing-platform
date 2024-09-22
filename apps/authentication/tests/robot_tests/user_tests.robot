*** Settings ***
Library    RequestsLibrary
Suite Setup   Set Base URL

*** Variables ***
${BASE_URL}  http://localhost:8000
${REGISTER_URL}  ${BASE_URL}/auth/register/
${LOGIN_URL}  ${BASE_URL}/auth/login/
${PROFILE_URL}  ${BASE_URL}/auth/profile/
${ADMIN_REGISTER_URL}  ${BASE_URL}/auth/admin/register/

*** Test Cases ***

Register New Customer User
    [Documentation]    Test the customer registration endpoint
    ${response}=    Create User    customer2    password123    customer1@example.com
    Should Be Equal As Strings    ${response.status_code}    201

Login with Customer User
    [Documentation]    Test customer login after registration
    ${response}=    Login User    customer1    password123
    Should Be Equal As Strings    ${response.status_code}    200

View Customer Profile
    [Documentation]    Test customer profile view
    ${response}=    Login User    customer1    password123
    Get Profile
    Should Be Equal As Strings    ${response.status_code}    200

Admin Creates New User
    [Documentation]    Test admin creating a new user
    ${admin_token}=  Login Admin    admin    admin_password
    ${response}=    Create User As Admin    admin    customer2    password123    customer2@example.com
    Should Be Equal As Strings    ${response.status_code}    201

*** Keywords ***

Set Base URL
    Create Session    authentication    ${BASE_URL}

Create User
    [Arguments]    ${username}    ${password}    ${email}
    ${data}=  Create Dictionary    username=${username}    password=${password}    email=${email}
    ${response}=    Post Request    authentication    ${REGISTER_URL}    json=${data}
    Log    Status code: ${response.status_code}
    Log    Response body: ${response.text}
    [Return]    ${response}

Login User
    [Arguments]    ${username}    ${password}
    ${data}=  Create Dictionary    username=${username}    password=${password}
    ${response}=    Post Request    authentication    ${LOGIN_URL}    json=${data}
    Log    ${response.text}
    [Return]    ${response}

Get Profile
    ${headers}=  Create Dictionary
    ${response}=    Get Request    authentication    ${PROFILE_URL}    headers=${headers}
    Log    ${response.text}
    [Return]    ${response}

Login Admin
    [Arguments]    ${admin_username}    ${admin_password}
    ${data}=  Create Dictionary    username=${admin_username}    password=${admin_password}
    ${response}=    Post Request    authentication    ${LOGIN_URL}    json=${data}
    ${token}=    Set Variable    ${response.json()['token']}
    [Return]    ${token}

Create User As Admin
    [Arguments]    ${admin_username}    ${username}    ${password}    ${email}
    ${admin_token}=  Login Admin    ${admin_username}    admin_password
    ${headers}=  Create Dictionary    Authorization=Bearer ${admin_token}
    ${data}=  Create Dictionary    username=${username}    password=${password}    email=${email}    role=customer
    ${response}=    Post Request    authentication    ${ADMIN_REGISTER_URL}    json=${data}    headers=${headers}
    Log    ${response.text}
    [Return]    ${response}
