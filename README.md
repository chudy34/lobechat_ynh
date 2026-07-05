# Lobe Chat for YunoHost

This repository packages [AIDotNet/lobe-chat](https://github.com/AIDotNet/lobe-chat) for YunoHost.

The package keeps YunoHost-specific files in this repository and builds Lobe Chat from a pinned upstream commit during install and upgrade. To follow upstream, update the pinned commit and package version with:

```bash
tools/update-upstream
```

Then test the package on a YunoHost server:

```bash
sudo yunohost app install https://github.com/chudy34/lobechat_ynh
sudo yunohost app upgrade lobechat -u https://github.com/chudy34/lobechat_ynh
```

## Current upstream

- Repository: `https://github.com/AIDotNet/lobe-chat`
- Commit: `d8950b27eaef10bdff72da894c8190a87a82a972`
- Lobe Chat version: `1.11.9`

## Notes

This package uses Docker CE + Compose v2 on the YunoHost server. Supporting services are managed by the package: PostgreSQL/ParadeDB, RustFS, Redis, and SearXNG.
