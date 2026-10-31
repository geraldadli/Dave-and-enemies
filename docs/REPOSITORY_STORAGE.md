# Repository storage

GameMaker resource metadata, runtime assets, editable art/audio sources, extracted
deliveries, import scripts, design data and validation reports belong in Git.
The project can be opened and built directly from those tracked files.

Keep compiled games, compiler caches, Python bytecode, delivery ZIP bundles,
review animations, audio review reels and individual runtime QA captures local.
The ignore rules cover these generated files. Existing local copies are retained
when they are removed from Git's index.

The ZIP bundles repeat files already available in the extracted deliveries.
Importers read the extracted folders, not the archives. Older handoff documents
may link to a local ZIP or review image; those links are optional delivery and
review conveniences, rather than build requirements. The extracted UI kit is in
`docs/ui/`, Dave deliveries are in `art/exports/dave/`, and production audio is in
`audio/music/`, `audio/sfx/` and `audio/voice/`.

Representative layout review boards remain tracked in
`design/desert/previews/`; the individual captured game frames are local. Review
JSON reports remain tracked. Layout boards can be regenerated with
`python tools/preview_desert_layouts.py`. Dave review tools are
`art/tools/review_dave_down.py` and `art/tools/review_dave_cardinal.py`.
`python tools/package_chapter_sfx.py` regenerates the SFX review reels.

Do not omit registered `sounds/`, `sprites/` or `tilesets/` resources merely to
reduce the file count. GameMaker needs their source images/audio and metadata.
Identical source and imported files share Git blob objects, even when both paths
appear in the checkout; deleting one identical copy does not necessarily reduce
Git transfer size.

Ignoring and untracking files prevents new commits from including them. Existing
commits retain their old blobs, so the approved cleanup replaces the initial
commit with a cleaned, parentless V.1.0 snapshot. Game assets and map changes
retain their original Git blob contents.

The original commit remains available through a local-only recovery reference
under `refs/local-backups/`. That reference is not pushed to the remote. Pushes
target `main` explicitly so new clones receive the cleaned history.
