import win32api
import win32security

import win32api
import win32security


def adjust_privileges(privileges_to_keep=None):
    if privileges_to_keep is None:
        privileges_to_keep = []
    try:
        # Get the current process token with adjust and query privileges
        current_process_token = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
        )

        # Get all privileges to disable
        all_privileges = win32security.GetTokenInformation(current_process_token, win32security.TokenPrivileges)

        # Filter the privileges to keep by privilege ID
        privileges_to_keep_ids = []
        for privilege_name in privileges_to_keep:
            privilege_id = win32security.LookupPrivilegeValue(None, privilege_name)
            privileges_to_keep_ids.append(privilege_id)

        # Construct a list of privileges to disable
        token_privileges = []
        for privilege in all_privileges:
            if privilege[0] not in privileges_to_keep_ids:
                new_state = (privilege[0], 4)  # 4 means give up the privilege
                token_privileges.append(new_state)

        # Apply the change of privileges
        win32security.AdjustTokenPrivileges(current_process_token, False, token_privileges)
        return True

    except Exception as e:
        return False
