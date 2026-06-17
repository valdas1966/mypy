# Instruction to AI Agent (Claude Code): Google Drive Operations

The authoritative how-to for every Google Drive operation in the MyPy
project. Connect with the VALDAS OAuth credentials.

## Read Drive Instructions First

Before performing **any** Google Drive operation (session work,
summaries, reports, LaTeX, uploads, reads, deletes, folder listings,
etc.), **always read the relevant file(s) from the Drive
`Instructions/` folder first**. This folder holds the authoritative,
up-to-date workflows — the local `CLAUDE.md` is only a pointer.

```python
from f_google.services.drive import Drive
drive = Drive.Factory.valdas()

# 1) Discover what instructions exist:
for f in drive.files(path='Instructions'):
    print(f)

# 2) Read the relevant one(s) for the task at hand:
print(drive.read(path='Instructions/For_Session_Summary.md').text)
print(drive.read(path='Instructions/For_Report.md').text)
print(drive.read(path='Instructions/For_Summary.md').text)
print(drive.read(path='Instructions/For_Tex.md').text)
```

Rules:
- **Never cache** these instructions across sessions — always re-read
  from Drive, since they may have been updated.
- Map task → instruction file:
  - Session start / session summary → `For_Session_Summary.md`
  - Paper / project reports → `For_Report.md`
  - Paper summaries → `For_Summary.md`
  - LaTeX, TikZ, graphs, figures → `For_Tex.md`
- If no dedicated instruction file matches the task, list
  `Instructions/` anyway and confirm — new instruction files may
  have been added.
- Follow the Drive instruction verbatim; if it conflicts with the
  local `CLAUDE.md`, **the Drive instruction wins**.

## How to Open Google Drive

Connect to our Google Drive using the VALDAS OAuth credentials:
```python
from f_google.services.drive import Drive
drive = Drive.Factory.valdas()
```

## Common Operations

**List folders and files:**
```python
folders = drive.folders(path='Projects/2026')   # list subfolder names
files = drive.files(path='Projects/2026')       # list file names
folders = drive.folders()                       # root-level folders
```

**Read a file into memory (no local save):**
```python
response = drive.read(path='Papers/Topic/Paper.pdf')
print(response.text)       # text content (markdown for PDFs)
print(response.pages)      # list[bytes] — PNG pages (PDFs only)
```

**Check existence:**
```python
if drive.is_exists(path='2026/04/07/session.md'):
    ...
```

**Upload (auto-creates parent folders, overwrites if exists):**
```python
drive.upload(path_src='/tmp/file.md',
             path_dest='2026/04/07/file.md')
```

**Download to local disk:**
```python
drive.download(path_src='Papers/Topic/Paper.pdf',
               path_dest='/tmp/Paper.pdf')
```

**Create folder / delete:**
```python
drive.create_folder(path='2026/04/07')
drive.delete(path='2026/04/07/old_file.md')
```

## Drive-Only Workflow

- **Never save Drive files locally** in the project directory.
- Use `/tmp/` for all intermediate work (compile, edit, etc.).
- Upload results back to Drive.
- Do **not** auto-open files — the user views them on Drive.
