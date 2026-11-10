"""Nondeterministic midpoint PDA simulation for palindromes over {a,b}."""
def is_palindrome_pda(word: str) -> bool:
    if any(ch not in "ab" for ch in word): return False
    n=len(word)
    for midpoint in range(n+1):
        for skip in (0,1):
            if skip and midpoint>=n: continue
            stack=list(word[:midpoint])
            right=word[midpoint+skip:]
            for ch in right:
                if not stack or stack.pop()!=ch: break
            else:
                if not stack: return True
    return False

def midpoint_traces(word: str):
    if any(ch not in "ab" for ch in word):
        return ["REJECT — alphabet must be {a,b}."]
    n=len(word)
    for midpoint in range(n+1):
        for skip in (0,1):
            if skip and midpoint>=n: continue
            stack=list(word[:midpoint]); right=word[midpoint+skip:]
            steps=[f"Guess midpoint after prefix '{word[:midpoint]}'.",
                   f"{'Skip centre symbol '+repr(word[midpoint]) if skip else 'Use an even split'}.",
                   f"Push phase complete: stack = {''.join(stack) or 'Z0'}."]
            failed=False
            for ch in right:
                if not stack or stack[-1]!=ch:
                    steps.append(f"Read '{ch}': mismatch; this branch rejects.")
                    failed=True; break
                stack.pop()
                steps.append(f"Read '{ch}': match and pop; stack = {''.join(stack) or 'Z0'}.")
            if not failed and not stack:
                steps.append("Input exhausted with bottom marker only: this branch accepts.")
                return steps
    return ["All possible midpoint choices reject: input is not a palindrome."]
