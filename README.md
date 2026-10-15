# Layerling for Unraid

Community-maintained Docker template for [Layerling](https://layerling.com/).
The application and image come from [henmedia/layerling](https://github.com/henmedia/layerling).
This repository supplies installation metadata and does not build the image.

## Installation settings

- Image: `ghcr.io/henmedia/layerling:latest`.
- Bridge networking; host port `3000` maps to container port `3000`.
- Web interface: `http://YOUR_UNRAID_IP:3000`.
- Shared designs: `/mnt/user/appdata/layerling/projects` maps to `/shared-projects`.
- `LAYERLING_SHARED_PROJECTS_DIR=/shared-projects` enables server storage.
- Runs as Unraid `nobody:users` (`99:100`) through `--user=99:100`.

Create/select a host projects directory writable by UID 99 and GID 100.
Layerling's upstream image normally runs as UID/GID 999; upstream documents
overriding the runtime user for writable bind mounts. Do not add PUID/PGID
variables: the upstream image does not document support for them.

Open **On the server** in Layerling to save shared designs. Designs saved in
the browser remain browser-local until moved. Back up the host projects folder.

## Before submitting to Community Apps

1. Create a public GitHub repository named `unraid-templates`, or choose another name.
2. The XML URLs use GitHub account `jbat66`. If you chose another
   repository name or branch, update all repository URLs too.
3. Enable GitHub Issues for template support, or replace Support with your own
   Unraid support thread. Keep application bug reports directed upstream.
4. Review the license and maintainer details. The MIT license here applies to
   these original template files; Layerling itself is AGPLv3, and upstream artwork
   retains its upstream licensing.
5. Upload this directory's contents to the repository root.
6. Test a fresh installation on Unraid with an empty projects directory. Verify
   WebUI access, saving and reopening a server design, and persistence after
   recreating the container. Verify writes work as UID 99/GID 100. Change the
   host port and confirm the WebUI shortcut still uses the mapped port.
7. Run **Validate** and **Scan** at https://ca.unraid.net/submit and resolve any
   findings, including category or icon requirements. Inspect the listing preview.
8. Submit for review after the checks pass.

The XML files have been checked for well-formedness locally. The container has
not been run or tested on Unraid, and the Community Apps scan has not been run.

## Changes from the supplied private template

- Kept the upstream image and set the default host port to 3000.
- Replaced the personal share path with a portable appdata default.
- Mounted the projects directory directly at `/shared-projects`, with the variable
  pointing at exactly that path, rather than mounting its parent at `/srv`.
- Added runtime user settings for the shared directory and documented permissions.
- Added project, support, readme, category, license, and template URL metadata.
- Removed installation-specific fields and shortened the listing description.

For the original mapping, the effective projects folder was the
`layerling-projects` subfolder beneath the host directory mounted at `/srv`.
If adapting this template to your existing installation, point the new host
mapping at that existing subfolder to keep the same designs visible. Publishing
these files does not change your existing container or move its data.

## References

- https://ca.unraid.net/submit/help
- https://github.com/unraid/unraid-community-apps-starter
- https://github.com/henmedia/layerling#docker
