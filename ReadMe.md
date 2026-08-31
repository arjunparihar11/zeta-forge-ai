# ZetaForge AI
ZetaForge AI is a full stack, single page interactive story engine that combines AI roleplay with a visual novel interface. It runs entirely in the browser using IndexedDB for persistence and the Gemini API for generation. Inspired by the zeta role play app.

## Features
| Feature | Description |
| :--- | :--- |
| **Multiple Scenario Management** | Create, switch, rename, and delete entire story timelines with independent cast, lore, and message history. |
| **Dual View Mode** | Toggle between Chat Feed (messenger style) and Visual Novel Stage (large sprites, backdrop, auto advance). |
| **Dramatis Personae Panel** | Sidebar lists Main Cast + dynamically detected Side Characters; click any to open a full spotlight. |
| **Character Spotlight** | View/edit persona, visual profile, current outfit, mood, intercharacter relationships, and AI generated chapter arc. |
| **Photo/Sprite Management** | Upload single photos, paste URLs, or upload a 4×4 sprite sheet that auto extracts 16 emotion sprites with background removal. |
| **AI Image Generation** | Generate 1:1 square character portraits (1024×1024) and 4096×4096 sprite sheets (4×4 grid) using Gemini Flash Image Preview. |
| **Scene Visualizer** | Generate a 16:9 cinematic illustration of the current scene, using character reference photos and story context. |
| **Lorebook/Codex** | Keyword triggered entries that auto inject relevant lore into the AI context only when needed. |
| **Chapter Chronicle** | Auto archives chapters when token limit is reached. Stories milestone summaries and per character arc summaries. |
| **Relationship Tracking** | AI detects significant events (confession, fight, reunion, etc.) and updates relationship labels between characters. |
| **Reply Suggestions** | AI generates 3 distinct dialogue/action options you can insert with one tap. |
| **Branch Editing** | Edit any message > deletes all subsequent turns and regenerates from that branch; undo supported. |
| **Import / Export** | Import plain‑text transcripts (auto‑parses speakers) or export full Markdown story logs. |
| **Full JSON Backup** | One click backup/restore of all scenarios, messages, lore, avatars, and metadata. |
| **PWA Ready** | Service worker, manifest, and touch optimized UI for mobile/desktop. |

---

## Program Outline

```
ZetaForge AI
├── UI Layer
│   ├── Header (Zeta logo, scenario title, view toggle, chapter badge)
│   ├── Left Sidebar (Cast list with avatars & moods)
│   ├── Right Drawers (Chapter Chronicle + Lorebook, Scenarios Menu)
│   ├── Main Canvas (Chat Feed / Visual Novel Stage)
│   └── Bottom Bar (Input, Narrate toggle, Suggest, Visualize, Continue)
│
├── Modals
│   ├── Setup (API key, model, cast, outfits, lorebook, user persona)
│   ├── Import (paste transcript)
│   ├── Character Spotlight (dossier with edit mode)
│   ├── Image Library (all generated scene visuals)
│   ├── Avatar Manager (upload/manage photos & sprite sheets)
│   └── Lightbox (full screen image preview)
│
├── Core Engine
│   ├── State Management (IndexedDB + localStorage)
│   ├── Scenario CRUD (create, switch, delete)
│   ├── Message Store (branching, editing, deletion)
│   ├── Typewriter Renderer (per character, per turn with skip support)
│   └── VN Stage Controller (turn navigation, auto play, backdrop)
│
├── AI Integration (Gemini API)
│   ├── System Prompt Builder (injects persona, outfits, lore, relationships)
│   ├── Call API (JSON structured multi turn replies)
│   ├── Character Arc Analyzer (summarizes each character's chapter journey)
│   ├── Relationship Updater (detects significant events, updates labels)
│   ├── Lorebook Auto Generator (extracts durable facts from story)
│   ├── Reply Suggester (3 distinct options)
│   ├── Image Generator (portraits, sprite sheets, scene visuals)
│   └── Chapter Archiver (auto triggers at token threshold)
│
└── Image Pipeline
    ├── Compression (client side WebP/JPEG resizing)
    ├── Sprite Sheet Splitter (4×4 grid > 16 sprites with background removal)
    └── Avatar/Photo Manager (upload, URL, set default, delete)
```
