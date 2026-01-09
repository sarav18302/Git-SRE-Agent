import re
import logging

class GitGuardrail:
    """Security layer to validate AI-generated shell commands."""
    
    DENY_LIST = [
        (r"rm\s+-rf\s+/", "Root directory deletion attempt"),
        (r"sudo", "Privilege escalation attempt"),
        (r"chmod\s+777", "Unsafe permission change"),
        (r"> /dev/sd", "Direct disk write attempt"),
        (r"git\s+gc\s+--prune", "Permanent history destruction")
    ]

    @classmethod
    def validate(cls, command: str):
        command = command.strip().split('\n')[0]
        
        # Check Deny List
        for pattern, reason in cls.DENY_LIST:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"🚨 BLOCKED: {reason}"

        # Logic Check: Force Pushing
        if "push" in command and "--force" in command:
            if "--force-with-lease" not in command:
                return False, "🚨 BLOCKED: Force push detected without '--force-with-lease'."

        return True, "✅ Command Authorized"