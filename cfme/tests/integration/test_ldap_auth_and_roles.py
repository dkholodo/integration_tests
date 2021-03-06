import pytest

from cfme.utils.appliance.implementations.ui import navigate_to
from cfme.utils.conf import credentials
from cfme.utils.testgen import auth_groups, generate

pytest_generate_tests = generate(gen_func=auth_groups, auth_mode='ldap')


@pytest.mark.uncollect('Needs to be fixed after menu removed')
@pytest.mark.tier(2)
def test_group_roles(
        request, appliance, configure_ldap_auth_mode, group_name, group_data, infra_provider):
    """Basic default LDAP group role RBAC test

    Validates expected menu and submenu names are present for default
    LDAP group roles


    Polarion:
        assignee: apagac
        caseimportance: medium
        initialEstimate: 1/4h
        tags: rbac
    """
    request.addfinalizer(appliance.server.login_admin)

    # This should be removed but currently these roles are subject to a bug
    if group_name in ['evmgroup-administrator',
                      'evmgroup-approver',
                      'evmgroup-auditor',
                      'evmgroup-operator',
                      'evmgroup-security',
                      'evmgroup-support',
                      'evmgroup-user']:
        pytest.skip("This role currently fails this test")

    try:
        username = credentials[group_name]['username']
        password = credentials[group_name]['password']
    except KeyError:
        pytest.fail('No match in credentials file for group "{}"'.format(group_name))

    user = appliance.collections.users.simple_user(username, password)
    with user:
        navigate_to(appliance.server, 'LoggedIn')
    # assert set(menu.nav.visible_pages()) == set(group_data)
