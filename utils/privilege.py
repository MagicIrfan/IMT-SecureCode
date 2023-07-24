import win32api
import win32security


def adjust_privileges():
    privileges_to_disable = [
        "SeAssignPrimaryTokenPrivilege",
        "SeAuditPrivilege",
        "SeBackupPrivilege",
        "SeChangeNotifyPrivilege",
        "SeCreateGlobalPrivilege",
        "SeCreatePagefilePrivilege",
        "SeCreatePermanentPrivilege",
        "SeCreateSymbolicLinkPrivilege",
        "SeCreateTokenPrivilege",
        "SeDebugPrivilege",
        "SeEnableDelegationPrivilege",
        "SeImpersonatePrivilege",
        "SeIncreaseBasePriorityPrivilege",
        "SeIncreaseQuotaPrivilege",
        "SeIncreaseWorkingSetPrivilege",
        "SeLoadDriverPrivilege",
        "SeLockMemoryPrivilege",
        "SeMachineAccountPrivilege",
        "SeManageVolumePrivilege",
        "SeProfileSingleProcessPrivilege",
        "SeRelabelPrivilege",
        "SeRemoteShutdownPrivilege",
        "SeRestorePrivilege",
        "SeSecurityPrivilege",
        "SeShutdownPrivilege",
        "SeSyncAgentPrivilege",
        "SeSystemtimePrivilege",
        "SeSystemEnvironmentPrivilege",
        "SeSystemProfilePrivilege",
        "SeTakeOwnershipPrivilege",
        "SeTcbPrivilege",
        "SeTimeZonePrivilege",
        "SeTrustedCredManAccessPrivilege",
        "SeUndockPrivilege",
        "SeDelegateSessionUserImpersonatePrivilege"
    ]

    current_process_token = win32security.OpenProcessToken(
        win32api.GetCurrentProcess(),
        win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
    )

    token_privileges = []

    for privilege_name in privileges_to_disable:
        try:
            # get privilege ID
            privilege_id = win32security.LookupPrivilegeValue(None, privilege_name)
            new_state = (privilege_id, 0)  # 0 means disable the privilege
            token_privileges.append(new_state)

        except Exception as e:
            return False

    # Apply the change of privileges
    try:
        win32security.AdjustTokenPrivileges(current_process_token, False, token_privileges)
        return True
    except Exception as e:
        return False
