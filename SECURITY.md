# Security reporting and scope

This experimental tool reports supported configuration changes. It is not a
complete supply-chain scanner, a proof of PR safety, or an unbypassable merge gate.

For a security issue in this tool, use GitHub private vulnerability reporting when
available. Otherwise open an issue requesting a private reporting channel without
including credentials, sensitive repository content, or exploit details. Public
issues are suitable for ordinary bugs and synthetic reproductions.

Install the Action from a reviewed full commit SHA, outside the proposed checkout.
Use read-only permissions and keep default-permission assertions under trusted
operator control. The advisory pilot must remain outside required merge checks.
