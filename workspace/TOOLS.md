# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Discord Webhooks

**Daily Standup Reports:**
- URL: `https://discordapp.com/api/webhooks/1475159106800062594/QI9DuxTmSrpXuuJDi4htNQBcKbWbZjrkfyXf-zrdfwBB8mad28WweQHxQ2vMZjWDnsUB`
- Channel: Status Reports
- Purpose: Daily status summaries from Grodd

---

### Google Workspace (gog)

**Account:** gorillagrodd73@gmail.com
**Setup completed:** 2026-02-22

**Environment variable required:**
```bash
export GOG_ACCOUNT=gorillagrodd73@gmail.com
```

**Quick commands:**
```bash
# List Drive files
gog drive ls --max 10

# Search Gmail
gog gmail search 'is:unread' --max 5

# Upload file
gog drive upload ~/Documents/file.pdf
```

**Note:** First API call after auth will take 30-60s to refresh token.

---

Add whatever helps you do your job. This is your cheat sheet.
