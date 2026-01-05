ROLE_PERMISSIONS = {
    "admin": {
        "members:read",
        "members:write",
        "projects:write",
        "projects:read",
    },
    "member": {
        "members:read",
        "projects:read",
    },
}


# Se le puede pasar una lista de roles
def has_permission(roles: list[str], permission: str) -> bool:
    for role in roles:
        if permission in ROLE_PERMISSIONS.get(role, set()):
            return True
    return False
