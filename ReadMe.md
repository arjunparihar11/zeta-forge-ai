# ZetaForge AI

ZetaForge AI is a single page interactive story engine. It joins AI roleplay with a visual novel stage. Everything runs in the browser and saves to IndexedDB. Story turns, images and voices come from Google Gemini, from models you host yourself or from both, with automatic fallback between them. The design takes cues from the Zeta roleplay app.

The whole app is one file, `index.html`. Tailwind and `marked` load from a CDN. There is no build step.

## Features

### Stories and scenarios

| Feature | Description |
| :--- | :--- |
| **Scenario management** | Create, switch, rename and delete story timelines. Each has its own cast, lore, calendar and message history. |
| **Recreate from a Zeta link** | Paste a zeta-ai.io plot link in the New Scenario drawer. ZetaForge reads the page, then the LLM you picked writes your own version with a persona, cast, outfits, lorebook, locations, start time, weather, calendar and relationships. If the page cannot be read automatically you can paste its text instead. |
| **AI Generate Scenario** | Describe the story you want, or let it invent one at random. It fills in the same fields as the link import, so a new scenario starts with every system already in use. |
| **Dual view** | Switch between a chat feed and a visual novel stage with large sprites, a backdrop, auto-advance and tap navigation. |
| **Branch editing** | Edit any message, delete the turns after it and regenerate from there. Every earlier wording is kept in the message history and can be restored. |
| **Import and export** | Import a plain text transcript, a Markdown file or a JSON backup. Export a Markdown transcript, an illustrated PDF or an illustrated EPUB with one chapter per Chronicle entry. |
| **Full JSON backup** | One click saves or restores scenarios, messages, lore, images and metadata. |

### Cast and characters

| Feature | Description |
| :--- | :--- |
| **Dramatis Personae** | The sidebar lists the main cast and side characters found during play. Click anyone to open a spotlight. |
| **Character spotlight** | View and edit persona, visual profile, outfit, mood, relationships and an AI written chapter arc. |
| **Relationship graph** | A diagram of the user and each main character. Tap a node to open that character. |
| **Photo and sprite library** | Upload photos, paste URLs or upload a 4x4 sprite sheet that splits into 16 emotion sprites, with a manual grid adjustment. |
| **Background removal** | Remove the background from one photo or from every photo in a character's library at once. It uses an AI segmentation model or a worker based fallback. |
| **Shot size** | Pick Full Body, 3/4, Half Body, Bust or Headshot before generating a character photo. |
| **Duplicate protection** | A generated photo labeled Default is stored once, not twice. |

### World systems

| Feature | Description |
| :--- | :--- |
| **Story clock** | A day and time tracker with weather and season. Skip ahead to a day or time of day, or set an exact time. Backdrops and music can follow the time of day. |
| **Calendar** | Add dated events that appear in the story context when they come due. |
| **Lorebook and Codex** | Entries are grouped as world, location, object or character. Keywords decide when an entry is sent to the model. Entries can be secret, built from templates, bulk imported or auto tagged. A token meter and a prompt preview show what will be sent. |
| **Locations** | A location picker with travel times. The current place shows in the top bar. |
| **Character schedules** | Characters can have a routine so the story knows who is likely to be where. |
| **Model driven tracker updates** | The model can report scene changes in a short tag that moves the clock, place and weather. |
| **Plot arcs** | Track long threads per scenario so the model keeps them in view. |
| **Chapter Chronicle** | Chapters archive when the token limit is reached. Each gets a summary and per character arc notes. Archiving can be undone from the panel or from the chapter divider in the story. |
| **Relationship tracking** | Significant events such as a confession, a fight or a reunion update relationship labels. Ordinary quiet stretches do not wear down stable ties. |

### AI routing and writing tools

| Feature | Description |
| :--- | :--- |
| **Multi-LLM routing** | Send turns to Gemini or to a self-hosted model on a workstation, Oracle Cloud or an iPad. Smart Auto-Routing tries each in order and uses the first that answers. |
| **Streamed turns** | Gemini and local turns stream in. Each character's line starts voice generation as soon as that line finishes. |
| **Suggest menu** | Reply suggestions, an Enhance option that rewrites your draft in place and a Create option for new ideas. Suggestions try the local model first and use Gemini only when a key is set. |
| **Visualize** | Draw the current scene from character reference photos and story context, with the same engine choices as portraits. |
| **Local-first maintenance** | Relationship checks and lorebook extraction try the local model first and fall back to Gemini. |
| **Context control** | Raw story data stays on the device. Only recent turns, recaps and keyword matched lore go to the model. Stable context can use Gemini context caching. |
| **Cost monitor** | Click the token counter in the Chronicle to see estimated text, portrait, sprite and scene costs. |

### Media

| Feature | Description |
| :--- | :--- |
| **Image generation** | Gemini Flash Image first, then a local MeinaMix server, then a public renderer. MeinaMix portraits keep a locked seed per character for a consistent look. |
| **Pixabay backdrops** | Search free photos and save them straight into the Backdrop Library. The panel suggests searches from the scenario text and the current location. A Pixabay API key is needed. |
| **Music browser** | Search Jamendo for full songs and Freesound for ambience, then save them to the Music Library. Jamendo needs a free client ID and Freesound needs an API key. |
| **Voice acting** | Three engines. Kokoro runs in the browser and sounds the most natural. Kitten TTS is the lightest. Chatterbox runs on your own machine with cloned voices. Auto picks whichever is reachable. Voice Lab can match or clone a voice per character. |
| **Speech input** | Dictate your turn with the microphone button on browsers that support it. |
| **Narration and mentions** | Start a line with `@:` to narrate as the scene. Use `@Name` to address a character. |
| **Dialogue formatting** | Actions and thoughts are wrapped in asterisks. The model is blocked from speaking as your persona on a turn you just typed. |

### Interface

| Feature | Description |
| :--- | :--- |
| **Top bar** | The title and scenario rows stay solid. The scene row (place, clock and a few shortcuts) floats over the story as pills. |
| **LLM status** | The bar under the chat shows the active model and a status dot. The same line is repeated in the Chronicle as the last engine used. |
| **Themes** | Dark and light modes. |
| **Storage** | Images are stored as blobs in IndexedDB and unused ones are cleaned up automatically, which keeps saves fast on long stories. |

---

## Self-Hosted AI Stack (optional)

ZetaForge works with only a Gemini API key. Every generation step can instead run on models you host, with Gemini kept as a fallback or left out.

- **LLM profiles** (Setup, then Routine Chat Inference): Workstation (Laptop), Oracle Cloud and iPad Air. Each has a URL, model name, optional key, context cap and ping target. A fourth choice, Smart Auto-Routing, pings them all and uses the first that responds. The Workstation profile accepts a LAN address and a Fallback URL such as a tunnel. Browsers block plain `http://` requests from an HTTPS page, so a LAN address only works when ZetaForge itself is opened over HTTP or from a local file. Use an HTTPS tunnel as the Fallback URL for everything else.
- **Companion scripts** (run on the machine that hosts your model):
  - `start_chatterbox_server.py` runs Chatterbox TTS with voice cloning.
  - `start_image_fallback_server.py` wraps a local SD1.5 and LCM-LoRA (MeinaMix) pipeline for image generation.
  - `reverse_proxy.py` puts the LLM (`/v1/*`), image fallback (`/image/*`) and Chatterbox TTS behind one port so one tunnel covers all three.
  - `ngrok_tunnel_core.bat` restarts LM Studio with CORS on, loads the model, starts the helper servers and opens an ngrok tunnel.
  - `cloudflare_tunnel_core.bat` does the same with Cloudflare Tunnel, which has no browser warning page.
  - `oracle_llm_setup.md` covers running a model on Oracle Cloud's free tier.
- **Google Colab option**: `Llama-3_1-Stheno_ZetaForge_Colab_Notebook.ipynb` runs a Stheno model on a Colab GPU and exposes it through ngrok. `launch_colab.py` opens the notebook and can try the Run all shortcut. `zeta_colab_server.py` is a single file version for a Colab cell. Your ngrok token is read from Colab secrets or an environment variable and is never stored in the repo.
- **Image fallback chain**: Gemini, then your local MeinaMix server, then pollinations.ai. Each step is tried when the one before is rate limited, refuses the scene or is not set up.
- **Known limit with free ngrok**: a free ngrok tunnel answers cross-origin preflight requests with its own warning page, which has no CORS headers, so the browser blocks the call. Use the Cloudflare launcher, a paid ngrok plan or another tunnel such as Tailscale Funnel.

---

## Program Outline

```
ZetaForge AI (index.html)
├── UI layer
│   ├── Top bar (logo, scenario title, view toggle, chapter badge, floating scene row)
│   ├── Left sidebar (cast list with avatars and moods)
│   ├── Right drawers (Chronicle, Lorebook, Scenarios, New Scenario, LLM connection)
│   ├── Main canvas (chat feed or visual novel stage)
│   └── Bottom bar (input, Narrate, Suggest, Visualize, Continue, Search)
│
├── Modals
│   ├── Setup (LLM profiles, keys, TTS, cast, outfits, user persona)
│   ├── Import, Character Spotlight, Chapter Chronicle
│   ├── Image Library, Avatar Manager, Voice Lab
│   ├── Pixabay browser, Music browser
│   ├── Relationship Graph, Message History, API Usage and Cost
│   └── Lightbox
│
├── Core engine
│   ├── State (IndexedDB with a localStorage fallback, debounced saves)
│   ├── Scenario model (cast, lorebook, plot arcs, calendar, world clock)
│   ├── Message store (undo snapshots for edits, branches and deletes)
│   ├── Typewriter renderer and VN stage controller
│   └── Long-term memory (raw archive, recaps, lore, selective context)
│
├── AI integration (Gemini and local endpoints)
│   ├── Endpoint resolver (Gemini, Workstation, Oracle, iPad, Smart Auto-Routing)
│   ├── System prompt builder and context cache manager
│   ├── Call layer (retry, backoff and streaming, no retry on client errors)
│   ├── Scenario builder (Zeta link import and AI generation)
│   ├── Background maintenance (relationship events, lorebook extraction, arcs)
│   ├── Reply suggester, Enhance and visual prompt writer
│   ├── Image generator (Gemini, local MeinaMix, public fallback)
│   └── Voice engine (Kokoro, Kitten, Chatterbox, Auto)
│
└── Image pipeline
    ├── Compression (worker with a main thread fallback)
    ├── Sprite sheet splitter (4x4 grid with manual adjustment)
    ├── Background removal (segmentation model or worker heuristic)
    ├── Blob asset store with garbage collection
    └── Photo manager (upload, URL, default, delete)
```

---

## Default Empty State

With no local data, ZetaForge starts a scenario named **Simulation** with **Bob** as the main and user character. Bob is a middle aged businessman who knows he is a test subject in a simulation. Existing local scenarios and imported data are kept, never replaced.

## Data and Privacy

Story state, characters, generated images, lorebook entries and raw messages are stored in the browser. Use the JSON backup to move or restore a story. API keys for Gemini, Pixabay and Freesound, the Jamendo client ID and local endpoint keys sit in the app's local state, so treat them as secrets. 

Two features contact outside services. The Zeta link import requests the public plot address (without the share code) from the site and from free page reader relays when direct reading is blocked. The app asks you to confirm once before the first relay request. The Pixabay, Jamendo and Freesound browsers send your search words to those services.

## Deployment

ZetaForge is a single `index.html` and can be deployed as is, for example to Render. Keep the branding files `zetaforge.svg` (top bar logo) and `zetaforge.png` (home screen icon) next to it. The `llm-icon-*.svg` files in the folder are not referenced by the page, which draws those icons inline, so they can be removed. The Python scripts, batch files and notebook run on your own machine or on Colab and are not served by the page.
