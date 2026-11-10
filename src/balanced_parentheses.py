"""Deterministic stack recognizer for balanced parentheses."""
def is_balanced_parentheses(text: str) -> bool:
    stack=[]
    for symbol in text:
        if symbol=="(": stack.append("(")
        elif symbol==")":
            if not stack: return False
            stack.pop()
        else: return False
    return not stack

def trace_parentheses(text: str):
    stack=[]; trace=[("START", "Z0")]
    for i,ch in enumerate(text,1):
        if ch=="(": stack.append("(")
        elif ch==")":
            if not stack:
                trace.append((f"read ')' at {i}","REJECT — empty stack")); return trace
            stack.pop()
        else:
            trace.append((f"read {ch!r} at {i}","REJECT — symbol outside alphabet")); return trace
        trace.append((f"read {ch!r} at {i}","Z0 "+ " ".join(stack) if stack else "Z0"))
    trace.append(("END","ACCEPT" if not stack else "REJECT — unmatched opening parenthesis"))
    return trace
