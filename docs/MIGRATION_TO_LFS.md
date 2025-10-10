# Migration to Git LFS — checklist

This document describes a safe process to migrate existing large files (for example, `problems/`) to Git LFS.

High-level approach
- Prepare: create a mirror backup of the repository.
- Prepare: add `.gitattributes` and enable Git LFS (we already did this for new commits).
- Test: run the migration locally in a fresh clone using `git lfs migrate import`.
- Verify: run tests and validate repository contents.
- Push: if verified, push rewritten branch with `--force-with-lease`.
- Notify: inform collaborators to re-clone or reset their local clones.

Prerequisites
- Git (latest stable)
- Git LFS installed and configured (`git lfs install`)
- Sufficient local disk space to clone and rewrite repository

Commands (summary)

1. Backup mirror (mandatory)

```powershell
git clone --mirror C:\path\to\repo repo-mirror.git
```

2. Create a working clone

```powershell
git clone C:\path\to\repo repo-lfs-migrate
cd repo-lfs-migrate
git lfs install
```

3. Add `.gitattributes` (if needed)

```powershell
# example .gitattributes content
problems/** filter=lfs diff=lfs merge=lfs -text
*.mexw64 filter=lfs diff=lfs merge=lfs -text
*.mat filter=lfs diff=lfs merge=lfs -text
```

4. Run migration (local/test)

```powershell
# This rewrites history locally
git lfs migrate import --include="problems/**" --include-ref=refs/heads/main
```

5. Verify

```powershell
git count-objects -vH
pytest -q
git lfs ls-files | Select-Object -First 20
```

6. Push rewritten branch (ONLY when verified)

```powershell
git push origin main --force-with-lease
```

7. Communicate to collaborators (example message)

"We migrated the repo to Git LFS and rewrote history to move large files into LFS. You must re-clone the repository or reset your local branches: `git fetch origin && git reset --hard origin/main`. If you have local branches with unpushed work, please back them up before syncing."

Notes and risks
- Rewriting history changes commit hashes.
- Open pull requests and forks may need manual intervention.
- Git LFS uses external storage; confirm quota on GitHub or your Git host.

If you want us to perform the migration, confirm with: `PROCEED LFS MIGRATE`.
