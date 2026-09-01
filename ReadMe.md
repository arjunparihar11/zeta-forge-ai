# ZetaForge AI
ZetaForge AI is a full stack, single page interactive story engine that combines AI roleplay with a visual novel interface. It runs entirely in the browser using IndexedDB for persistence and the Gemini API for generation. Inspired by the zeta role play app.

## Features
| Feature | Description |
| :--- | :--- |
| **Multiple Scenario Management** | Create, switch, rename, and delete entire story timelines with independent cast, lore, and message history. |
| **Dual View Mode** | Toggle between Chat Feed (messenger style) and Visual Novel Stage (large sprites, backdrop, auto advance). |
| **Dramatis Personae Panel** | Sidebar lists Main Cast & dynamically detected Side Characters. Click any to open a full spotlight. |
| **Character Spotlight** | View/edit persona, visual profile, current outfit, mood, intercharacter relationships, and AI generated chapter arc. |
| **Photo/Sprite Management** | Upload single photos, paste URLs, or upload a 4×4 sprite sheet that auto extracts 16 emotion sprites with optional background removal. |
| **AI Image Generation** | Generate 1:1 square character portraits (1024×1024) and 4096×4096 sprite sheets (4×4 grid) using Gemini Flash Image. |
| **Scene Visualizer** | Generate a 16:9 cinematic illustration of the current scene, using character reference photos and story context. |
| **Lorebook/Codex** | Keyword triggered entries that auto inject relevant lore into the AI context only when needed, capped to the strongest matches. |
| **Chapter Chronicle** | Auto archives chapters when token limit is reached, with chapter summaries and per character arc summaries. |
| **Relationship Tracking** | AI detects significant events (confession, fight, reunion, breakup, etc.) and updates relationship labels without degrading stable family/social relationships during ordinary inactivity. |
| **Reply Suggestions** | AI generates 3 distinct dialogue/action options with scene aware caching to avoid redundant calls. |
| **Branch Editing** | Edit any message, delete subsequent turns, and regenerate from that branch. Undo supported. |
| **Import / Export** | Import plaintext transcripts (auto parses speakers) or export full Markdown story logs. |
| **Full JSON Backup** | One click backup/restore of all scenarios, messages, lore, avatars, metadata, and raw story history. |
| **Long Term Local Memory** | Full raw story data remains locally stored while compact context, recaps, and relevant lore are selectively sent to Gemini to reduce token usage. |
| **Context Caching** | Stable story/persona context can use Gemini context caching while dynamic dialogue remains outside the cache. |
| **Cost & Token Monitor** | Click the Chapter Chronicle token counter to view estimated text, portrait, sprite sheet, and scene generation costs. |
| **PWA Ready** | Service worker, manifest, PNG/SVG app icon, and touch optimized UI for mobile/desktop. |

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
│   ├── API Usage & Cost (estimated per-turn and image costs)
│   └── Lightbox (full screen image preview)
│
├── Core Engine
│   ├── State Management (IndexedDB + localStorage fallback)
│   ├── Scenario CRUD (create, switch, rename, delete)
│   ├── Message Store (branching, editing, deletion)
│   ├── Typewriter Renderer (per character, per turn with skip support)
│   ├── VN Stage Controller (turn navigation, auto play, backdrop)
│   └── Long-Term Memory (raw archive, recaps, lore, selective context)
│
├── AI Integration (Gemini API)
│   ├── System Prompt Builder (persona, relationships, relevant lore)
│   ├── Context Cache Manager (stable-prefix caching with fallback)
│   ├── Call API (structured multi-turn replies with retry/backoff)
│   ├── Character Arc Analyzer
│   ├── Significant-Event Relationship Updater
│   ├── Lorebook Auto Generator
│   ├── Reply Suggester with scene cache
│   ├── Visual Prompt Cache
│   ├── Image Generator (portraits, sprite sheets, scene visuals)
│   └── Chapter Archiver / Recap Compaction
│
└── Image Pipeline
    ├── Compression (client side WebP/JPEG resizing)
    ├── Sprite Sheet Splitter (4×4 grid > 16 sprites)
    ├── Optional Background Removal
    └── Avatar/Photo Manager (upload, URL, set default, delete)
```

## Default Empty State
When no local ZetaForge data exists, the application initializes a fresh scenario named **Simulation** with **Bob** as the default main/user character. Bob is described as a middle aged businessman who is aware that he is a test subject in a simulation. Existing local scenarios and imported data are preserved rather than replaced.

## Data & Privacy
Story state, character data, generated avatars, lorebook entries, and raw messages are stored locally in the browser. Full JSON backup/export can be used to move or restore a story. The Gemini API key is kept in the application's local state and should be treated as a secret.

## Deployment
ZetaForge AI is designed as a single page `index.html` application. The repository should also contain the branding assets referenced by the page, including `zetaforge.svg` for the top-bar logo and `zetaforge.png` for the PWA/home-screen icon.
