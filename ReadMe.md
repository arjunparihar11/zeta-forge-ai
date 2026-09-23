# ZetaForge AI

ZetaForge AI is a full-stack, single-page interactive story engine that combines AI roleplay with a visual novel interface. It runs entirely in the browser using IndexedDB for persistence, and can generate story turns, images, and voice through Google Gemini and/or your own self-hosted models — with automatic fallback between them. Inspired by the zeta roleplay app.

## Features

| Feature | Description |
| :--- | :--- |
| **Multiple Scenario Management** | Create, switch, rename, and delete entire story timelines with independent cast, lore, and message history. |
| **Dual View Mode** | Toggle between Chat Messenger (turn feed) and Visual Novel Stage (large sprites, backdrop, auto-advance, left/right tap navigation). |
| **Multi-LLM Routing** | Route story generation to Gemini or to your own self-hosted models — a home Workstation, Oracle Cloud, or an iPad — with automatic LAN-first/tunnel-fallback addressing and an Auto profile that probes and picks whichever is reachable. |
| **Local-First Reply Suggestions & Scene Prompts** | Suggested Replies and the Visualize scene-prompt writer try your active local LLM before ever touching Gemini, instead of requiring a Gemini key. |
| **Dramatis Personae Panel** | Sidebar lists Main Cast and dynamically detected Side Characters. Click any to open a full spotlight. |
| **Character Spotlight** | View and edit persona, visual profile, current outfit, mood, inter-character relationships, and an AI-generated chapter arc. |
| **Photo and Sprite Management** | Upload single photos, paste URLs, or upload a 4×4 sprite sheet that auto-extracts 16 emotion sprites, with optional background removal and manual grid-adjustment for sheets that don't line up perfectly. |
| **AI Image Generation with Local Fallback** | Generate 1:1 square character portraits and 4×4 sprite sheets via Gemini Flash Image, or switch to a locally-hosted MeinaMix/SD1.5 fallback (single-pose portrait prompting, no Gemini key required) at generation time — with a final anonymous public-renderer fallback if neither is available. |
| **Scene Visualizer** | Generate a cinematic illustration of the current scene using character reference photos and story context, with the same Gemini/local engine choice as character photos. |
| **Voice Acting (TTS)** | Three interchangeable engines — Kokoro (~85MB, in-browser, most expressive), Kitten TTS (~25–80MB, in-browser, lightest), and Chatterbox (Laptop, best quality, runs on your own machine with cloned voices) — plus an Auto mode that picks whichever is actually reachable. Voice Lab supports AI voice matching and Gemini-assisted voice cloning per character. |
| **Lorebook and Codex** | Keyword-triggered entries that auto-inject relevant lore into the AI context only when needed. Background maintenance auto-extracts new durable facts from recent story turns on a rolling cadence (a missed check retries every subsequent turn instead of waiting a full interval), with an explicit per-entry schema so extracted keywords stay actually searchable later. |
| **Chapter Chronicle** | Auto-archives chapters when the token limit is reached, with AI-generated chapter summaries and per-character arc summaries. Archiving (manual or automatic) can be undone from the Chronicle panel or by tapping the chapter divider chip inline in the story. |
| **Relationship Tracking** | AI detects significant events (confession, fight, reunion, breakup, etc.) and updates relationship labels without degrading stable family or social relationships during ordinary inactivity. |
| **Reply Suggestions** | AI generates distinct dialogue and action options, trying your active local LLM first with a scene-aware cache, falling back to Gemini only when a key is present. |
| **Branch Editing** | Edit any message (correctly reverting to the original text on Undo), delete subsequent turns, and regenerate from that branch or retry the last turn. |
| **Narration & Mentions** | Use `@:` to narrate as the scene itself, or `@Name` to mention a character — rendered without the leading `@` so mentions read like natural prose while the underlying stored text stays exact for search. |
| **Dialogue Formatting Enforcement** | The AI is instructed (and its output is post-processed) to wrap actions/thoughts in asterisks consistently, and is hard-blocked from voicing the user's own persona on a turn the user just typed — Continue and the opening scene are the only points it may narrate on the user's behalf. |
| **Import and Export** | Import plaintext transcripts (auto-parses speakers) or export full Markdown story logs. |
| **Full JSON Backup** | One-click backup and restore of all scenarios, messages, lore, avatars, metadata, and raw story history. |
| **Long-Term Local Memory** | Full raw story data remains locally stored while compact context, recaps, and relevant lore are selectively sent to the active LLM to reduce token usage. |
| **Context Caching** | Stable story and persona context can use Gemini context caching while dynamic dialogue remains outside the cache. |
| **Cost and Token Monitor** | Click the Chapter Chronicle token counter to view estimated text, portrait, sprite sheet, and scene generation costs. |
| **PWA Ready** | Service worker, manifest, PNG and SVG app icon, and touch-optimized UI for mobile and desktop. |

---

## Self-Hosted AI Stack (optional)

ZetaForge works with just a Gemini API key, but every generation surface — story turns, reply suggestions, image generation, and voice — can instead be routed to models you run yourself, with Gemini available only as an explicit fallback (or not used at all).

- **LLM profiles** (Setup → Routine Chat Inference): **Workstation (Laptop)**, **Oracle Cloud**, and **iPad Air**, each with its own URL, model name, optional API key, context cap, and ping target, plus an **Auto** profile that pings all of them and uses whichever responds. The Workstation profile additionally supports a LAN address tried first and a **Fallback URL** (e.g. an ngrok/tunnel address) tried if the LAN address isn't reachable — this matters because ZetaForge is served over HTTPS, and browsers block a plain `http://` LAN request from an HTTPS page outright (Mixed Content policy). Point the Fallback URL at an HTTPS tunnel to route around this from anywhere, not just your home network.
- **Companion scripts** (run on the machine hosting your local model, not tracked as part of the deployed app):
  - `start_chatterbox_server.py` — Chatterbox TTS server with voice cloning support.
  - `start_image_fallback_server.py` — a Flask server wrapping a local SD1.5 + LCM-LoRA (MeinaMix) pipeline for fast local image generation; accepts optional width/height/negative-prompt overrides so the same server serves both wide scene visuals and single-pose character portraits correctly.
  - `reverse_proxy.py` — combines the LLM (`/v1/*`), image-gen fallback (`/image/*`), and Chatterbox TTS (everything else) behind a single local port, so one tunnel URL covers all three services.
  - `ngrok_tunnel_core.bat` — one-shot Windows launcher: restarts LM Studio's server with CORS enabled, loads the model, starts Chatterbox and the image-gen fallback server in the background, starts the reverse proxy, then opens the ngrok tunnel.
  - `oracle_llm_setup.md` — setup notes for running a model on Oracle Cloud's free tier as the Oracle Cloud profile's backend.
- **Image generation fallback chain**: Gemini (default) → your configured local MeinaMix server → an anonymous public renderer (pollinations.ai), tried in that order whenever the previous tier is rate-limited, refuses a scene, or isn't configured.
- **Known limitation**: a free ngrok tunnel serves its own browser-warning interstitial page to any cross-origin request that needs a CORS preflight (i.e. any JSON POST — which is most requests here), and that interstitial has no CORS headers, so the browser blocks the request before it reaches your server. This affects local LLM and image-gen calls made *through* a free ngrok tunnel from the HTTPS-deployed app. Workarounds: a paid ngrok plan (removes the interstitial), or a tunnel tool that doesn't inject one (e.g. Cloudflare Tunnel, Tailscale Funnel).

---

## Program Outline
```
ZetaForge AI
├── UI Layer
│   ├── Header (Zeta logo, scenario title, view toggle, chapter badge)
│   ├── Left Sidebar (Cast list with avatars and moods)
│   ├── Right Drawers (Chapter Chronicle, Lorebook, and Scenarios Menu)
│   ├── Main Canvas (Chat Feed / Visual Novel Stage)
│   └── Bottom Bar (Input, Narrate toggle, Suggest, Visualize, Continue)
│
├── Modals
│   ├── Setup (LLM profiles, API keys, TTS engine, cast, outfits, lorebook, user persona)
│   ├── Import (paste transcript)
│   ├── Character Spotlight (dossier with edit mode)
│   ├── Chapter Chronicle (archive/undo, cost & context, per-character arcs)
│   ├── Image Library (all generated scene visuals)
│   ├── Avatar Manager (upload and manage photos and sprite sheets)
│   ├── Voice Lab (voice matching and cloning per character)
│   ├── API Usage and Cost (estimated per-turn and image costs)
│   └── Lightbox (full-screen image preview)
│
├── Core Engine
│   ├── State Management (IndexedDB and localStorage fallback)
│   ├── Scenario CRUD (create, switch, rename, delete)
│   ├── Message Store (deep-cloned undo snapshots on edit; branching, editing, deletion)
│   ├── Typewriter Renderer (per character, per turn, with skip support and user-persona-speech enforcement)
│   ├── VN Stage Controller (turn navigation, auto-play, backdrop)
│   └── Long-Term Memory (raw archive, recaps, lore, selective context)
│
├── AI Integration (Gemini + local LLM endpoints)
│   ├── Endpoint Resolver (Gemini vs. Workstation/Oracle Cloud/iPad Air/Auto, LAN-first with tunnel fallback)
│   ├── System Prompt Builder (persona, relationships, relevant lore, formatting rules)
│   ├── Context Cache Manager (stable prefix caching with fallback)
│   ├── Call API (structured multi-turn replies with retry, backoff, and streaming for local models)
│   ├── Character Arc Analyzer
│   ├── Significant Event Relationship Updater
│   ├── Lorebook Auto-Extractor (rolling cadence, schema-constrained keywords)
│   ├── Reply Suggester (local-first, scene-cached, Gemini fallback)
│   ├── Visual Prompt Writer (local-first, Gemini fallback)
│   ├── Image Generator (Gemini → local MeinaMix → public fallback, portraits/sprite sheets/scene visuals)
│   ├── Voice Engine (Kokoro/Kitten in-browser, Chatterbox on your laptop, Auto selection)
│   └── Chapter Archiver, Undo, and Recap Compaction
│
└── Image Pipeline
    ├── Compression (client-side WebP and JPEG resizing)
    ├── Sprite Sheet Splitter (4×4 grid into 16 sprites, with manual grid adjustment)
    ├── Optional Background Removal
    └── Avatar and Photo Manager (upload, URL, set default, delete)
```

---

## Default Empty State
When no local ZetaForge data exists, the application initializes a fresh scenario named **Simulation** with **Bob** as the default main and user character. Bob is described as a middle-aged businessman who is aware that he is a test subject in a simulation. Existing local scenarios and imported data are preserved rather than replaced.

## Data and Privacy
Story state, character data, generated avatars, lorebook entries, and raw messages are stored locally in the browser. Full JSON backup and export can be used to move or restore a story. Any API keys (Gemini or a local endpoint's own key) are kept in the application's local state and should be treated as secrets. When routing to a self-hosted endpoint over a public tunnel, treat that tunnel URL as sensitive too, since anyone with it can reach your local model server.

## Deployment
ZetaForge AI is designed as a single-page `index.html` application, deployable as-is (e.g. to Render). The repository should also contain the branding assets referenced by the page (`zetaforge.svg` for the top-bar logo and `zetaforge.png` for the PWA/home-screen icon), plus the optional companion Python scripts and batch launcher described above if you intend to use the self-hosted AI stack — those run on your own machine and are not served by the deployed page itself.
