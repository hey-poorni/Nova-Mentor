---
description: Commit and push all changes to GitHub after task completion
---

// turbo-all

## Commit and Push to GitHub

After completing any task, follow these steps to commit and push changes:

1. Stage all changed files
```
git -C "e:\Projects E\Novamentor\src\Nova-Mentor" add -A
```

2. Commit with a descriptive message (replace `<message>` with something meaningful like the task description)
```
git -C "e:\Projects E\Novamentor\src\Nova-Mentor" commit -m "<message>"
```

3. Push to GitHub
```
git -C "e:\Projects E\Novamentor\src\Nova-Mentor" push origin main
```

4. Confirm the push was successful by checking the remote log
```
git -C "e:\Projects E\Novamentor\src\Nova-Mentor" log --oneline -5
```
