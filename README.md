<p align="center">
  <img src="https://i.imgur.com/s8cY7lu.png" alt="YAAP Central BOT">
</p>

<h1 align="center">YAAP Central BOT</h1>

<p align="center">
  The internal Discord bot powering the <strong>YAAP Brasil</strong> community — automating support, role requests, and advising flows so the team can focus on what truly matters: the people.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/discord.py-2.x-5865F2?logo=discord&logoColor=white" alt="discord.py">
  <img src="https://img.shields.io/badge/status-archived-lightgrey" alt="Archived">
</p>

---

## About YAAP

**YAAP Brasil** (Young Academic Ambassadors Project) is an international non-profit youth organization whose mission is to democratize access to international opportunities for Brazilian youth — with a special focus on low-income, peripheral, and interior-region young people.

Through education, leadership, and inclusion, YAAP believes it's possible to build a future where Brazilian youth can reach their full potential and transform their communities and the world.

> *"Construir uma comunidade onde jovens tenham acesso igualitário a oportunidades que antes pareciam inalcançáveis."*

---

## About This Project

YAAP Central BOT was built to support the day-to-day operations of the YAAP Discord server, automating support ticket flows, role assignment requests, advising scheduling, and administrative tools — so the volunteer team spends less time managing threads and more time helping people.

As a server-specific bot, it contains hardcoded channel and role IDs tailored to YAAP's server structure.

---

## Features

### 🎫 Support Ticket System
A persistent button in the support channel creates a dedicated thread for the user upon click. The staff is notified, the conversation is handled within the thread, and it's closed with the `!encerrar` command.

### 📋 Role Request System
A thread-based flow for users to request server roles. After opening a request, the user provides the necessary information (full name, approval proof, role) and the staff reviews it manually.

### 🎓 Advising (Pre-College & College)
An advising scheduling system with a modal form. The user fills in their name, email, and goal, and a thread is created with the information for the responsible advisor team.

### 🛠️ Administrative Tools
- **`/embed`** — Interactive custom embed builder
- **`!falar`** — Sends a message or file to a specified channel as the bot

### 🎵 Study Room Music
The bot automatically joins the study voice channel when someone is present, playing audio files on random rotation. It disconnects on its own when the channel becomes empty.

### 🔁 Inactivity Check
A background task runs every hour checking open threads in the support channels. Threads with no activity for over 48 hours are automatically archived, locked, and deleted after a warning.

---

## Structure

```
YAAP-Central-BOT/
├── main.py                  # Bot entry point, inactivity task, permission check
├── cogs/
│   ├── administracao.py     # Administrative commands (embed, falar)
│   ├── advising.py          # Advising system with modals and threads
│   ├── cargos.py            # Role request flow via thread
│   ├── musica.py            # Automatic music in the study room
│   ├── suporte.py           # Support ticket system via thread
│   └── owner.py             # Owner-only commands (sync)
└── utils/
    ├── emojis.py            # Custom server emoji mapping
    └── musicas/             # Audio files for the study room
```

---

## Commands

| Command | Description | Access |
|---|---|---|
| `!suporte` | Posts the support panel with a ticket button | Admin |
| `!encerrar` | Closes and deletes the current support thread | Inside ticket |
| `!cargos` | Posts the role request panel | Admin |
| `!precollege` | Posts the Pre-College Advising panel | Admin |
| `!college` | Posts the College Advising panel | Admin |
| `!resolvido` | Marks a forum post as resolved | Post owner |
| `/embed` | Opens the interactive embed builder | Admin |
| `!falar` | Sends a message to a channel as the bot | Admin |
| `!sync` | Syncs slash commands with Discord | Owner |

---

## Tech Stack

- **Python** — Primary language
- **discord.py 2.x** — Bot framework
- **FFmpeg** — Audio playback in the study room
- **python-dotenv** — Environment variable management

---

## Notes

- This bot is **exclusive to the YAAP server** and has hardcoded channel, role, and thread IDs throughout the codebase.
- The permission system checks for the `admin` role or the owner's ID before executing any command.
- Persistent button views (`PersistentTickets`, `PersistentCargos`, `PersistentAdvising`) are re-registered on startup to survive bot restarts.
