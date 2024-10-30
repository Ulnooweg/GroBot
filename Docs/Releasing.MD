# Releasing instructions
This file list steps to make a proper release specific to this project.

1. Make sure the [changelog file](/Docs/CHANGELOG.MD) is updated with the version about to be released and thet the [setup file](/Docs/Setup.md) is updated with appropriate instructions for release version.
2. Following proper procedures as outlined in the [contributing document](/Docs/CONTRIBUTING.md), merge all code for that release into main.
3. Copy the folder `code` and `systemd_bootfile` under the `Software` folder into another folder called `Release`. Zip the folder `Release` into a zip file called `Release.zip`.
4. Delete the file `grobot_cfg.ini` from the `code` folder and rename the folder `Release` to `Release-keepsettings`. Zip the folder `Release-keepsettings` into a zip file called `Release-keepsettings.zip`.
5. Using the appropriate tool, get the file hash in SHA-512 format for both `Release-keepsettings.zip` and `Release.zip` file.
   - For Windows, use powershell with the command:
     > Get-FileHash "<PATH>" -Algorithm SHA512 | Format-List
6. Create a release:
   * Titled `Release vx.y.z` as appropriate
   * Body contains `GroBot software update version x.y.z` as first line in the body.
   * List all changes under `Changes:` using information from the [changelog file](/Docs/CHANGELOG.MD).
   * In the `Note:` section, it should contain:
     - `Please consult \[setup file]\(https://github.com/TNarakol-UEC/GroBot/blob/v1.0.4/Docs/Setup.md) for instructions on software installations.` where v1.0.4 is the release version.
     - `The software file \`Release.zip\` can be verified by the SHA-512 checksum: ...CHECKSUM...`
     - `The software file \`Release-keepsettings.zip\` can be verified by the SHA-512 checksum: ...CHECKSUM...`
7. Add the 2 zip files `Release.zip` and `Release-keepsettings.zip` as a binary to the release.
8. Set target to main and the tag to be `v1.0.4` where v1.0.4 represent the release version.
9. Now release.