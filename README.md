# LobeHub for YunoHost

This repository packages [lobehub/lobehub](https://github.com/lobehub/lobehub) for YunoHost.

The package keeps YunoHost-specific files in this repository and runs the official LobeHub Docker image pinned to the current upstream release. To follow upstream, update the pinned Docker image tag and package version with:

```bash
tools/update-upstream
```

GitHub Actions also runs this updater every day and pushes a commit when a newer upstream release exists.

Then test the package on a YunoHost server:

```bash
sudo yunohost app install https://github.com/chudy34/lobechat_ynh
sudo yunohost app upgrade lobehub -u https://github.com/chudy34/lobechat_ynh
```

## Current upstream

- Repository: `https://github.com/lobehub/lobehub`
- Release: `v2.2.9`
- Docker image: `lobehub/lobehub:2.2.9`
- LobeHub version: `2.2.9`

## Notes

This package uses Docker CE + Compose v2 on the YunoHost server. Supporting services are managed by the package: PostgreSQL/ParadeDB, RustFS, Redis, and SearXNG.
