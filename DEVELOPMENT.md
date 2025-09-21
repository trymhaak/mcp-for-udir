# Development Workflow

## Branch Structure

- **main** - Production-ready releases only (protected)
- **development** - Integration branch for features
- **feature/[name]** - Individual feature development
- **hotfix/[name]** - Critical bug fixes for production

## Version Control Workflow

### Starting New Feature Development

```bash
# Always start from updated development branch
git checkout development
git pull origin development

# Create feature branch
git checkout -b feature/your-feature-name

# Work on your feature...
# Commit regularly with clear messages
git add .
git commit -m "Add: specific feature description"
```

### Feature Completion

```bash
# Before merging, ensure your branch is up to date
git checkout development
git pull origin development
git checkout feature/your-feature-name
git rebase development

# Test that everything still works
docker build -t udir_api-mcp-server:test .
# Run your tests...

# Merge to development
git checkout development
git merge feature/your-feature-name
git branch -d feature/your-feature-name
```

### Creating Releases

```bash
# From development branch, create release
git checkout development
# Update VERSION file
echo "1.1.0" > VERSION
git add VERSION
git commit -m "Bump version to 1.1.0"

# Merge to main and tag
git checkout main
git merge development
git tag -a v1.1.0 -m "Release v1.1.0: Description of changes"

# Build release Docker image
docker build -t udir_api-mcp-server:v1.1.0 .
docker tag udir_api-mcp-server:v1.1.0 udir_api-mcp-server:latest
```

### Emergency Hotfixes

```bash
# Create hotfix from main
git checkout main
git checkout -b hotfix/critical-bug-fix

# Fix the issue, test thoroughly
# ...

# Update VERSION (patch version)
echo "1.0.1" > VERSION
git add .
git commit -m "Hotfix: Description of fix"

# Merge to both main and development
git checkout main
git merge hotfix/critical-bug-fix
git tag -a v1.0.1 -m "Hotfix v1.0.1: Critical bug fix"

git checkout development
git merge hotfix/critical-bug-fix
git branch -d hotfix/critical-bug-fix
```

## Rollback Strategy

### Quick Rollback to Last Working Version

```bash
# View available versions
git tag -l

# Rollback to specific version
git checkout v1.0.0

# Rebuild Docker image with stable version
docker build -t udir_api-mcp-server:rollback .
docker tag udir_api-mcp-server:rollback udir_api-mcp-server:latest

# Update Docker MCP Gateway to use rollback image
# (Docker will automatically use the :latest tag)
```

### Emergency Recovery

```bash
# If development branch is broken, create new branch from last stable
git checkout v1.0.0
git checkout -b emergency-recovery

# Make minimal fixes
# Test thoroughly
# Follow hotfix workflow above
```

## Docker Image Versioning

### Development Images
```bash
# For testing during development
docker build -t udir_api-mcp-server:dev .
```

### Release Images
```bash
# Tag with version and latest
docker build -t udir_api-mcp-server:v1.1.0 .
docker tag udir_api-mcp-server:v1.1.0 udir_api-mcp-server:latest
```

### Testing New Features
```bash
# Build test image
docker build -t udir_api-mcp-server:test .

# Test in isolated environment before updating latest tag
```

## Commit Message Conventions

- **Add:** New features or capabilities
- **Update:** Improvements to existing features
- **Fix:** Bug fixes
- **Remove:** Removing features or code
- **Refactor:** Code restructuring without functional changes
- **Docs:** Documentation updates
- **Test:** Adding or updating tests

## Backup Current Working State

```bash
# Before major changes, create backup tag
git tag -a backup-$(date +%Y%m%d) -m "Backup before major changes"
```

## Integration Testing

Before any release:

1. Build Docker image
2. Test all three MCP tools (fetch_resource, get_by_id, search_resources)
3. Verify Claude Desktop integration
4. Check error handling with invalid requests
5. Validate API endpoint connectivity

## Current Status

- **Version:** 1.0.0 (tagged as v1.0.0)
- **Current Branch:** development
- **Last Stable:** v1.0.0 on main branch
- **Docker Image:** udir_api-mcp-server:latest

## Safe Development Rules

1. **Never commit directly to main**
2. **Always test before merging to development**
3. **Tag every release**
4. **Keep VERSION file updated**
5. **Document breaking changes**
6. **Test Docker integration after changes**